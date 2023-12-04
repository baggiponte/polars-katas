<h1 align="center">🐻‍❄️ Polars Katas</h1>

<div align="center">
    <i>
        In data's embrace,<br>
        Polars' dance, a swift, fine art,<br>
        Mastery's soft grace.
    </i>
</div>

---

![polar-youngling](./public/polars-katas.png)

## 🍱 Preparations for this Journey

1. Install [`PDM`](https://pdm-project.org/latest/#recommended-installation-method) or any other PEP-517 PEP-518 compliant package manger (basically, not `poetry`).

> **Note**
>
> **Recommended way to install Python CLIs**
>
> `pip install [--user] <lib>` can mess up with your system python (even when used with the `--user` flag).
> It is better to use a tool such as `pipx`, that will install every executable in a sandboxed environment.

```bash
pipx install pdm
```

2. Install the dependencies

```bash
# basically, just installs polars
pdm install

# install jupyter as well
pdm install -G ide
```

3. Launch an IDE, a REPL or a Jupyter notebook to run the katas. Execute the following cell to import Polars and a list of URLs that contain the data. We'll use the NYC Taxi dataset. We can get the links of the data from February to September 2023 only, since they have the same format. The source is [here](https://www1.nyc.gov/site/tlc/about/tlc-trip-record-data.page).

```python
import polars as pl

base = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2023-{:02d}.parquet"

# we keep the files from Feb 2023 to retain those with the same schema
urls = tuple(base.format(month) for month in range(2, 10))
```

4. Get the weather data

Data can be retrieved from `./data/weather.csv`, or through this script:

<details>

```bash
pdm install -G data
```

```python
import openmeteo_requests

import requests_cache
import polars as pl
from retry_requests import retry

# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after = -1)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)

# Make sure all required weather variables are listed here
# The order of variables in hourly or daily is important to assign them correctly below
url = "https://archive-api.open-meteo.com/v1/archive"
params = {
	"latitude": 40.7143,
	"longitude": -74.006,
	"start_date": "2023-02-01",
	"end_date": "2023-11-30",
	"hourly": ["temperature_2m", "relative_humidity_2m", "precipitation", "rain", "snowfall", "snow_depth", "weather_code", "wind_speed_10m", "wind_speed_100m"]
}
responses = openmeteo.weather_api(url, params=params)

# Process first location. Add a for-loop for multiple locations or weather models
response = responses[0]
print(f"Coordinates {response.Latitude()}°E {response.Longitude()}°N")
print(f"Elevation {response.Elevation()} m asl")
print(f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")
print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")

# Process hourly data. The order of variables needs to be the same as requested.
hourly = response.Hourly()
hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
hourly_relative_humidity_2m = hourly.Variables(1).ValuesAsNumpy()
hourly_precipitation = hourly.Variables(2).ValuesAsNumpy()
hourly_rain = hourly.Variables(3).ValuesAsNumpy()
hourly_snowfall = hourly.Variables(4).ValuesAsNumpy()
hourly_snow_depth = hourly.Variables(5).ValuesAsNumpy()
hourly_weather_code = hourly.Variables(6).ValuesAsNumpy()
hourly_wind_speed_10m = hourly.Variables(7).ValuesAsNumpy()
hourly_wind_speed_100m = hourly.Variables(8).ValuesAsNumpy()

hourly_data = {"date": pd.date_range(
	start = pd.to_datetime(hourly.Time(), unit = "s"),
	end = pd.to_datetime(hourly.TimeEnd(), unit = "s"),
	freq = pd.Timedelta(seconds = hourly.Interval()),
	inclusive = "left"
)}
hourly_data["temperature_2m"] = hourly_temperature_2m
hourly_data["relative_humidity_2m"] = hourly_relative_humidity_2m
hourly_data["precipitation"] = hourly_precipitation
hourly_data["rain"] = hourly_rain
hourly_data["snowfall"] = hourly_snowfall
hourly_data["snow_depth"] = hourly_snow_depth
hourly_data["weather_code"] = hourly_weather_code
hourly_data["wind_speed_10m"] = hourly_wind_speed_10m
hourly_data["wind_speed_100m"] = hourly_wind_speed_100m

hourly_dataframe = pl.DataFrame(data = hourly_data)
```

</details>

## Kata 1: Eager Mode

* Read the first parquet file in the list using `pl.read_parquet`.
* Display the top five rows.

How long does this take?

<details>
<summary>🔎 Solution</summary>

```python
import polars as pl

url = urls[0]

pl.read_parquet(url).head()
```
</details>

## Kata 2: Lazy mode

Repeat the exercise above, using `pl.scan_parquet` instead. What happens if you run the code? What changes if you scan the whole set of URLs?

Write the code to materialize the result.

<details>
<summary>🔎 Solution</summary>

```python
pl.scan_parquet(url).head().collect()

pl.scan_parquet(urls).head()
```
</details>

## Kata 3: The schema

Display the `LazyFrame` schema.

Like `pandas`, `Polars` can `describe` the dataset. Can you do that on a `LazyFrame`?

<details>
<summary>🔎 Solution</summary>

```python
data = pl.scan_parquet(urls)

data.schema
```
</details>

## Kata 4: Selecting columns

Use `pl.select()` context to get the following columns:

1. Select all columns
2. Select all columns except `VendorID`.
3. Select all columns that contain `amount` in their name
4. Select all `Int64` columns.
5. Select all `Int64` and `Int32` columns.
5. Select all numeric columns.
6. Select all datetime and string columns, minus the first column.

> **Hint**. To inspect the intermediate steps or results of a query, you can always call the `fetch()` method. It is like a debug statement.

<details>
<summary>🔎 Solution</summary>

```python
data = pl.scan_parquet(urls)

# 1. Select all columns
data.select(pl.all())
data.select("*")
# 2. Select all columns except `VendorID`.
data.select(pl.all().except("VendorID"))
# 3. Select all columns that contain `amount` in their name
data.select(pl.col(r"^*amount$"))
# 4. Select all integer columns.
data.select(pl.col(pl.Int64))
# 5. Select all numeric columns.
data.select(pl.col(pl.NUMERIC_DTYPES))
# 6. Select all datetime and string columns.
data.select(pl.col(pl.DateTime), pl.col(pl.Utf8))
```
</details>

## Kata 5: Column Selectors

Use `selectors` to implement the previous selections, and the following ones:

7. Select all columns that are integers or datetime, except the first one.
8. Select all columns that contain an "ID" or "amount" and are not floating point numbers.

```python
import polars.selectors as cs
```

<details>
<summary>🔎 Solution</summary>

```python

# 1. Select all columns
data.select(cs.all())
# 2. Select all columns except `VendorID`.
data.select(~cs.by_name("VendorID"))
# 3. Select all columns that contain `amount` in their name
data.select(cs.contains("amount"))
data.select(cs.matches("*amount"))
# 4. Select all integer columns.
data.select(cs.integer())
# 5. Select all numeric columns.
data.select(cs.numeric())
# 6. Select all datetime and string columns.
data.select(cs.temporal(), cs.string())
data.select(cs.temporal() | cs.string())
# 7. Select all columns that are integers or datetime, except the first one.
data.select(cs.integer() - cs.first() | cs.temporal())
# 8. Select all columns that contain an "ID" or "amount" and are not floating point numbers.
data.select(cs.contains(("ID", "Amount")) | ~cs.float())
```
</details>

## Kata 6: Introduction to expressions

We already used expressions, such as `pl.col()` or `pl.all()`. These operations, that start with `pl.`, can only be evaluated inside a context.
Outside of one, they can be assigned to a variable or be used as return value of a function and still retain all query optimisations.

1. Multiply the `trip_distance` by 1000 to cast it in metres and name it `trip_distance_meters`.
2. Add `tolls_amount`, `Airport_fee` and name it `total_fees`.
3. Compute the ratio between `tip`, `total_fees`, `mta_tax` and `fare_amount` over `total_amount`.
4. Compute the average trip distance.
5. Count the different values of `passenger_count`.
6. Get the number of unique values of `VendorID` and `RatecodeID`.

> **Hint**. You can call `.alias` on an expression to rename the column it generates. Similarly, you can access the `.name.suffix` method to add a suffix. Alternatively, you can name the column using a kwarg notation (i.e., `col=pl.some.expr`).

<details>
<summary>🔎 Solution</summary>

```python
# 1. Multiply the `trip_distance` by 1000 to cast it in metres.
data.with_columns(trip_distance_meters = pl.col("trip_distance") * 1000)
data.with_columns(pl.col("trip_distance").mul(1000).alias("trip_distance_meters"))
data.with_columns(pl.col("trip_distance").mul(1000).name.suffix("_meters"))
# 2. Add `tolls_amount`, `Airport_fee` and name it `total_fees`.
data.with_columns(total_fees=pl.col("tolls_amount") + pl.col("Airport_fee")))
# 3. Compute the ratio between `tip`, `mta_tax` and `fare_amount` over `total_amount`.
data.with_columns(pl.col("tip", "mta_tax", "fare_amount").truediv("total_amount").name.suffix("_pct"))
# 4. Compute the average trip distance.
data.with_columns(pl.col("trip_distance").mean())
# 5. Count the unique values of `passenger_count`.
data.with_columns(pl.col("passenger_count").value_counts())
# 6. Get the unique values of `VendorID` and `RatecodeID`.
data.with_columns(pl.col("VendorID", "RatecodeID").n_unique())
```
</details>

## Kata 7: The query plan

The `LazyFrame` represents a *Logical Plan*, i.e. a sequence of transformations. It embodies a query, rather than a `DataFrame`. You can inspect this plan when you print the `repr` of the `LazyFrame`.

* What method does it suggest to call, to inspect the optimized plan?
* Inspect the plan of the last exercise of the previous kata, comparing the optimised and unoptimised queries.
* If you have `graphviz` on your `$PATH`, do the same with `data.show_graph`.

<details>
<summary>🔎 Solution</summary>

```python
percentage_change = pl.col("tip", "mta_tax", "fare_amount").truediv("total_amount").with_suffix("_pct")
data.with_columns(percentage_change).explain(optimized=True)
data.with_columns(percentage_change).explain(optimized=True)
```
</details>

## Kata 8: Chaining multiple contextes

Try to write the expressions in the sixth kata in the same `with_column` context. Do you notice any errors popping up? Can you explain them?

Call `explain` on both and compare the query plans.

<details>
<summary>🔎 Solution</summary>

```python
data.with_columns(
    pl.col("trip_distance").mul(1000).name.suffix("_meters"),
    pl.col("tolls_amount").add(pl.col("Airport_fee")).alias("total_fees"),
).with_columns(
    pl.col("tip_amount", "total_fees", "mta_tax", "fare_amount").truediv(pl.col("total_amount")).name.suffix("_pct")
).explain()
```
</details>

## Kata 9: Data types

You can change the memory representation of a numeric datatype with `.cast()`.

1. Cast the string column into a categorical.
1. Cast the integer columns to have the smallest memory footprint.

<details>
<summary>solution</summary>

```python
data.select(
    cs.temporal().as_expr().cast(pl.Date),
    cs.string().as_expr().cast(pl.Categorical),
    cs.numeric().shrink_dtype()
)
```
</details>

## Kata 10: Namespaces

Polars segregates operations on similar data types behind namespaces, e.g. `str`, `dt`, `list` and `struct`.

1. Cast the `store_and_fwd_flag` column to lowercase.
2. Extract the year, month and day of the temporal columns.
3. Cast the temporal columns to strings.
  1. Split them at the ` ` (space) mark
  2. Take the first element
  3. Split the element at the `-` mark.
  4. Cast the result into a struct.
  5. Cast the struct into a JSON string with.

<details>
<summary>solution</summary>

```python
data.select(
    cs.temporal().as_expr()
    .cast(pl.Utf8)
    .str.split(" ")
    .list.first()
    .str.split("-")
    .list.to_struct()
    .struct.json_encode()
).fetch()
```
</details>

## Kata 10: Filtering

Filtering, combined with the query optimiser, can translate in huge gains. Thanks to the so-called "predicate pushdown", query engines can scan parquet files to just read the required rows - thus saving bandwidth and I/O.

Filtering is done inside the `filter` context and uses basic Python logical operators. Perform the following filtering operations:

1. Passenger count is greater than 3.
2. The dropoff hour is the same as the pickup's.
2. Trip distance is greater than the average trip distance.

<details>
<summary>solution</summary>

```python

```
</details>

## Kata 11: Aggregations

Aggregations with `group_by` can be elegantly expressed in Polars. An aggregation looks like this: `data.group_by(...).agg(...)`. Inside the brackets, there can be any expression!

1. Aggregate by passenger count and compute the average and standard deviation of the trip distance.
2. Aggregate by month and compute the mean and standard deviation of the total price and trip distance.
3. Take the logs (base 10) of the price and round it to the nearest tenth. Use this to aggregate by price order of magnitude and compute the average and standard deviation of passengers and trip distance.
4. Aggregate by vendor ID and just write `"passenger_count` inside the `.agg` context. What happens?

<details>
<summary>solution</summary>

```python

```
</details>

