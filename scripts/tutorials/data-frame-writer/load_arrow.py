from dataclasses import dataclass
from typing import List, Tuple, Optional, Union
from pathlib import Path

import struct
import pyarrow as pa
import io

@dataclass(frozen=True)
class _BatchInfo:
    index: int
    start: int
    end: int
    num_rows: int

def _read_batch_metadata(path: str | Path, end: Optional[int]) -> List[_BatchInfo]:
    MAGIC = b"ARROW1"
    MAGIC_LEN = len(MAGIC)
    FOOTER_SIZE_LEN = 4
    CONTINUATION_MARKER = b"\xff\xff\xff\xff"

    from flatbuffers import encode
    import flatbuffers.number_types as N

    with pa.memory_map(str(path), 'r') as f:
        assert f.read(MAGIC_LEN) == MAGIC, "Not a valid Arrow IPC file"
        f.seek(-(FOOTER_SIZE_LEN + MAGIC_LEN), io.SEEK_END)
        footer_size = struct.unpack("<i", f.read(FOOTER_SIZE_LEN))[0]
        assert f.read(MAGIC_LEN) == MAGIC, "Invalid end magic"
        f.seek(-(FOOTER_SIZE_LEN + MAGIC_LEN + footer_size), 2)
        footer_buf = bytearray(f.read(footer_size))

    root_offset = encode.Get(N.UOffsetTFlags.packer_type, footer_buf, 0)
    tab_start = root_offset
    vtable_offset = tab_start - encode.Get(N.SOffsetTFlags.packer_type, footer_buf, tab_start)
    vtable_len = encode.Get(N.VOffsetTFlags.packer_type, footer_buf, vtable_offset)

    def field_offset(buf, field_index, vtab_len, vtab_off):
        slot = 4 + field_index * 2
        if slot >= vtab_len:
            return 0
        return encode.Get(N.VOffsetTFlags.packer_type, buf, vtab_off + slot)

    rb_field_offset = field_offset(footer_buf, 3, vtable_len, vtable_offset)
    if rb_field_offset == 0:
        return []

    vec_offset_pos = tab_start + rb_field_offset
    vec_offset = vec_offset_pos + encode.Get(N.UOffsetTFlags.packer_type, footer_buf, vec_offset_pos)
    num_blocks = encode.Get(N.UOffsetTFlags.packer_type, footer_buf, vec_offset)

    batch_info: List[_BatchInfo] = []
    row_offset = 0

    with open(path, "rb") as f:
        for i in range(num_blocks):
            block_start = vec_offset + 4 + i * 24
            block_offset = struct.unpack_from("<q", footer_buf, block_start)[0]
            f.seek(block_offset)
            marker = f.read(len(CONTINUATION_MARKER))
            meta_size = struct.unpack("<i", f.read(4) if marker == CONTINUATION_MARKER else marker)[0]
            msg_buf = bytearray(f.read(meta_size))

            msg_root = encode.Get(N.UOffsetTFlags.packer_type, msg_buf, 0)
            msg_vtab_off = msg_root - encode.Get(N.SOffsetTFlags.packer_type, msg_buf, msg_root)
            msg_vtab_len = encode.Get(N.VOffsetTFlags.packer_type, msg_buf, msg_vtab_off)

            header_off = field_offset(msg_buf, 2, msg_vtab_len, msg_vtab_off)
            if header_off == 0:
                raise ValueError("Could not find a valid header offset in Arrow file.")

            header_pos = msg_root + header_off
            rb_root = header_pos + encode.Get(N.UOffsetTFlags.packer_type, msg_buf, header_pos)
            rb_vtab_off = rb_root - encode.Get(N.SOffsetTFlags.packer_type, msg_buf, rb_root)
            rb_vtab_len = encode.Get(N.VOffsetTFlags.packer_type, msg_buf, rb_vtab_off)

            length_off = field_offset(msg_buf, 0, rb_vtab_len, rb_vtab_off)
            if length_off == 0:
                raise ValueError("Found batch with no rows. Verify file integrity.")

            num_rows = struct.unpack_from("<q", msg_buf, rb_root + length_off)[0]
            batch_info.append(_BatchInfo(index=i, start=row_offset, end=row_offset + num_rows - 1, num_rows=num_rows))
            row_offset += num_rows

    return batch_info

def _slice_indices(batch_info: List[_BatchInfo], start: int, end: int) -> Tuple[List[int], int, int]:
    if start < 0 or end > batch_info[-1].end or start > end:
        raise IndexError(f"Range [{start}, {end}] is out of bounds. Valid range: [0, {batch_info[-1].end}]")

    if start == 0 and end == batch_info[-1].end:
        return list(range(len(batch_info))), 0, batch_info[-1].num_rows

    batch_indices = []
    first_idx = last_idx = None

    for i, batch in enumerate(batch_info):
        if batch.end < start:
            continue
        batch_indices.append(batch.index)
        if first_idx is None:
            first_idx = i
        if batch.end >= end:
            last_idx = i
            break

    first_offset = 0 if first_idx is None else start - batch_info[first_idx].start
    last_offset = (batch_info[batch_indices[-1]].num_rows if last_idx is None
                   else end - batch_info[last_idx].start)

    return batch_indices, first_offset, last_offset

def load_arrow_file(
    filepath: Union[str, Path],
    start: Optional[int] = None,
    end: Optional[int] = None,
    columns: Optional[List[str]] = None
) -> pa.Table:
    """
    Load rows [start, end) from an Arrow IPC file as a PyArrow Table.

    Args:
        filepath: Path to the .arrow file.
        start:    First row index to include. Defaults to 0.
        end:      Last row index to include. Defaults to all rows.
        columns:  Column names to return. Defaults to all columns.

    Returns:
        PyArrow.Table containing the requested rows and columns.
    """
    filepath = Path(filepath)
    start = start or 0
    batches = _read_batch_metadata(filepath, end)

    if not batches:
        raise ValueError(f"No valid batches found in {filepath}")

    end = end if end is not None else batches[-1].end
    batch_indices, first_offset, last_offset = _slice_indices(batches, start, end)

    source = pa.memory_map(str(filepath), 'r')
    reader = pa.ipc.open_file(source)

    if not batch_indices:
        schema = reader.schema
        if columns:
            schema = pa.schema([f for f in schema if f.name in columns])
        return pa.Table.from_arrays([], schema=schema)

    def _batches():
        for i, batch_idx in enumerate(batch_indices):
            batch = reader.get_batch(batch_idx)
            if columns is not None:
                batch = batch.select(columns)
            if i == 0 or i == len(batch_indices) - 1:
                s = first_offset if i == 0 else 0
                e = last_offset if i == len(batch_indices) - 1 else batch.num_rows
                batch = batch.slice(s, e - s)
            yield batch

    return pa.Table.from_batches(_batches())
