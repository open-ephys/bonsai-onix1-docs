import pyarrow as pa

input_path = r"./path/to/corrupted_file.arrow"
output_path = r"./path/to/fixed_file.arrow"

with pa.memory_map(input_path, 'r') as f:
    magic = f.read(8)
    if magic != b'ARROW1\x00\x00':
        raise ValueError('Not an Arrow file.')

    with pa.ipc.open_file(f) as reader:
        schema = reader.schema
        num_batches = 0

        with pa.ipc.new_file(output_path, schema) as writer:
            for i in range(reader.num_record_batches):
                try:
                    batch = reader.get_batch(i)
                    writer.write_batch(batch)
                    num_batches += 1
                except (pa.ArrowInvalid, OSError) as e:
                    print(f"Skipped batch {i}: {e}")

        print(f"Recovered {num_batches} out of {reader.num_record_batches} batches from {input_path}, saved to {output_path}")