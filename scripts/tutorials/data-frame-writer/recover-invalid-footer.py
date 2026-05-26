import pyarrow as pa

input_path = r"./path/to/corrupted_file.arrow"
output_path = r"./path/to/fixed_file.arrow"

with pa.memory_map(input_path, 'r') as f:
    magic = f.read(8)
    if magic != b'ARROW1\x00\x00':
        raise ValueError('Not an Arrow file.')

    with pa.ipc.open_stream(f) as reader:
        schema = reader.schema
        num_batches = 0

        with pa.ipc.new_file(output_path, schema) as writer:
            while True:
                try:
                    batch = reader.read_next_batch()
                    writer.write_batch(batch)
                    num_batches += 1
                except StopIteration:
                    print(f"Read {num_batches} batches from corrupted file.")
                    break
                except (pa.ArrowInvalid, OSError) as e:
                    print(f"Stopped reading at batch {num_batches}: {e}")
                    break

    print(f"Recovered {num_batches} batches from {input_path}, saved to {output_path}")