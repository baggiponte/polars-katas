import polars as pl
import os
import glob

data_source = os.path.join("data", "taxi")

# Get a list of all parquet files in the directory
parquet_files = glob.glob(os.path.join(data_source, "*.parquet"))

# Read each file into a dataframe and concatenate them
#data = pl.concat([pl.scan_parquet(file) for file in parquet_files])

print(pl.read_parquet(parquet_files[0]).head())
