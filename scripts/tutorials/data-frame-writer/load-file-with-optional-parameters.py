from load_arrow import load_arrow_file

table = load_arrow_file("memory-monitor_0.arrow", start=100, end=5000, columns=['Clock', 'PercentUsed'])