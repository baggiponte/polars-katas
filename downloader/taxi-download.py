import polars as pl
import requests
import os

base = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2023-{:02d}.parquet"

# we keep the files from Feb 2023 to retain those with the same schema
urls = tuple(base.format(month) for month in range(2, 10))

# Define the directory to save the files
data_dir = os.path.join("..", "data", "taxi")

# Check if the directory exists, if not, create it
if not os.path.exists(data_dir):
    os.makedirs(data_dir)

# Loop over the URLs
for url in urls:
    # Send a GET request to the URL
    response = requests.get(url)

    # Get the file name from the URL
    file_name = url.split("/")[-1]

    # Define the path to save the file
    file_path = os.path.join(data_dir, file_name)

    # Save the content of the response as a file
    with open(file_path, "wb") as file:
        file.write(response.content)