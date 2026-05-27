import numpy as np
from load_arrow import load_arrow_file

table = load_arrow_file("npix-v1e-lfp_0.arrow")

data_cols = [name for name in table.schema.names if "LfpData" in name]
data = np.column_stack([table[col].to_numpy() for col in data_cols])
clock = table["Clock"].to_numpy()

stride = 12  # 30 kHz primary rate / 2.5 kHz LFP rate for NeuropixelsV1

mask = np.zeros(len(clock), dtype=bool)
mask[::stride] = True

data_unique = data[mask]    # shape: (num_unique_lfp_samples, num_channels)
clock_unique = clock[mask]  # acquisition clock counts at each unique LFP sample