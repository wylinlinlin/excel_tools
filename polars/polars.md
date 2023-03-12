### usage

```python
import polars as pl
df = pl.read_csv("x.csv", infer_schema_length=0).with_columns(pl.all().cast(pl.Utf8, strict=False))
```

#### 1. query rows

```python
df.filter(pl.col("col_name") == "conditions")  # single exact query
df.filter((pl.col("id") <= 2) & (pl.col("size") == "small"))  # multi exact query
df.filter(pl.col("col_name").str.contains("conditions"))  # fuzzy query
df.filter(pl.col("col_name").str.starts_with("A"))  # start with query
df.filter(pl.col("CMTE_ID").str.ends_with("32906"))  # end with query
```

#### 2. query columns

```python
df.select("col_name")  # single
df.select(["col1", "col2"])  # multi

df.find_idx_by_name("col_name")  # column's location
```

#### 3. get str length

```python
df.with_columns(pl.col("col_name").str.n_chars().alias("add_col_name"))  # 
```

#### 4. replace

```python
df.with_columns(pl.col("col_name").str.replace("old", "new"))  # replace first match
df.with_columns(pl.col("col_name").str.replace_all("old", "new"))  # replace all match

df.replace("col_name", pl.Series([10, 20, 30]))  # replace one column
df.replace_at_idx(0, pl.Series("col_namee", [10, 20, 30]))  # replace 1st column
```

#### 5. split

```python
df.with_columns(
    [
        pl.col("col_name")
        .str.splitn("/", 3)
        .struct.rename_fields(["1st_part", "2nd_part", "3rd_part"])
        .alias("fields"),
    ]
).unnest("fields").head()
```

#### 6. slice

```python
df.with_columns(pl.col("col_name").str.slice(0, length=3).alias("add"))  # str[0:3]
```

#### 7. switch str lower or upper

```python
df.with_columns(pl.col("col_name").str.to_lowercase().alias("add"))  # to lower
df.with_columns(pl.col("col_name").str.to_uppercase().alias("add"))  # to upper
```

#### 8. convert date format

```python
df.with_columns(
    pl.col("col_name")
    .str.strptime(pl.Date, "%m/%d/%Y", strict=False)  # %m/%d/%Y -> %Y-%m-%d
    .alias("date")
).head()

df.with_columns(pl.col("date").dt.day().alias("day"))  # get day
df.with_columns(pl.col("date").dt.month().alias("month"))  # get month
df.with_columns(pl.col("date").dt.year().alias("year"))  # get year
```

#### 9. merge

```python
pl.concat(
    [df_h1, df_h2,], 
    how="horizontal",  # by rows
)

pl.concat(
    [df_d1, df_d2,], 
    how="diagonal",  # by colums
)

df.join(other_df, on="ham", how="left")  # vlookup
```

#### 10. delete column

```python
df.drop("col_name")
df.drop(["col1", "col2"])
```

#### 11. fill null value

```python
df.fill_null(0)
```

#### 12. groupby

```python
df.groupby("a").agg(pl.col("b").sum())
```

#### 13. insert column

```python
df.insert_at_idx(0, pl.Series("add", [i for i in range(len(df))]))
```

#### 14. rename column

```python
df.rename({"old": "new"})
```

#### 15. sort

```python
df.sort(["c", "a"], descending=True)  # r -> df
df.sort("c", "a", descending=[False, True])  # r -> df
```

#### 16. duplicate

```python
df.unique(subset="col_name")
df.unique(subset=["col1", "col2"])
```

#### 17. dtype

```python
df.with_columns(pl.col("col_name").cast(pl.Int32))  # int32
df.with_columns(pl.col("col_name").cast(pl.Float64))  # float64
df.with_columns(pl.col("col_name").cast(pl.Utf8))  # str
```

