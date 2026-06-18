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
    df = pd.read_csv(RAW, encoding="latin-1")
    return df


def tidy_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Turn 'Order Date' into 'order_date' so columns are easy to type."""
    df.columns = (
        df.columns.str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("-", "_")
    )
    return df


def parse_dates(df: pd.DataFrame) -> pd.DataFrame:
    """The dates arrive as text like '11/8/2023' — make them real dates."""
    df["order_date"] = pd.to_datetime(df["order_date"], format="%m/%d/%Y")
    df["ship_date"] = pd.to_datetime(df["ship_date"], format="%m/%d/%Y")
    return df


def drop_unneeded(df: pd.DataFrame) -> pd.DataFrame:
    """row_id is just a counter and country is always 'United States'."""
    df = df.drop(columns=["row_id", "country"], errors="ignore")
    return df


def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    df = df.drop_duplicates()
    return df


def drop_empty_rows(df: pd.DataFrame) -> pd.DataFrame:
    """Some exports include blank rows with no real data — drop them."""
    df = df.dropna(subset=["sales"])
    return df


def fix_missing(df: pd.DataFrame) -> pd.DataFrame:
    """Some rows (Burlington, Vermont) have no postal_code."""
    df["postal_code"] = df["postal_code"].fillna(0).astype(int)
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
