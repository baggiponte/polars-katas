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

## Kata 1: Eager Mode

* Read the first parquet file in the list using `pl.read_parquet`.
* Display the top five rows.

How long does this take?

<details>
<summary>Solution</summary>

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
<summary>Solution</summary>

```python
pl.scan_parquet(url).head().collect()

pl.scan_parquet(urls).head()
```
</details>

## Kata 3: The schema

Display the `LazyFrame` schema.

Like `pandas`, `Polars` can `describe` the dataset. Can you do that on a `LazyFrame`?

<details>
<summary>Solution</summary>

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

<details>
<summary>Solution</summary>

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
<summary>Solution</summary>

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

```python
import polars as pl

url = urls[0]

pl.scan_parquet(0).head().collect()
```
</details>


