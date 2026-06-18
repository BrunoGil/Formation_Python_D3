"""Step 1 — Clean the raw Superstore data.

Fill in each `# TODO`, then run:

    python src/clean.py

When it works it writes a tidy file to output/clean.csv.
Tip: run `python src/explore.py` first to see what's messy.
"""
from pathlib import Path

import pandas as pd

RAW = Path("data/Sample - Superstore.csv")
OUT = Path("output/clean.csv")


def load_raw() -> pd.DataFrame:
    # TODO: read RAW into `df` with pandas, encoding="latin-1" (the file is Windows-encoded)
    return df


def tidy_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Turn 'Order Date' into 'order_date' so columns are easy to type."""
    # TODO: lower-case the columns, strip spaces, replace ' ' and '-' with '_'
    return df


def parse_dates(df: pd.DataFrame) -> pd.DataFrame:
    """The dates arrive as text like '11/8/2023' — make them real dates."""
    # TODO: pd.to_datetime on order_date and ship_date with format="%m/%d/%Y"
    return df


def drop_unneeded(df: pd.DataFrame) -> pd.DataFrame:
    """row_id is just a counter and country is always 'United States'."""
    # TODO: drop columns row_id and country (use errors="ignore")
    return df


def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    # TODO: drop exact duplicate rows
    return df


def drop_empty_rows(df: pd.DataFrame) -> pd.DataFrame:
    """Some exports include blank rows with no real data — drop them."""
    # TODO: drop rows that have no sales value (dropna with subset=["sales"])
    return df


def fix_missing(df: pd.DataFrame) -> pd.DataFrame:
    """Some rows (Burlington, Vermont) have no postal_code."""
    # TODO: fill missing postal_code with 0, then cast the column to int
    return df


def main() -> None:
    df = load_raw()
    df = tidy_columns(df)
    df = parse_dates(df)
    df = drop_unneeded(df)
    df = remove_duplicates(df)
    df = drop_empty_rows(df)
    df = fix_missing(df)

    OUT.parent.mkdir(exist_ok=True)
    df.to_csv(OUT, index=False)
    print(f"Wrote {len(df)} clean rows -> {OUT}")
    print(df.dtypes)


if __name__ == "__main__":
    main()
