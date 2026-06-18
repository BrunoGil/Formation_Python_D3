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
    #--SOLUTION:read RAW into `df` with pandas, encoding="latin-1" (the file is Windows-encoded)
    df = pd.read_csv(RAW, encoding="latin-1")
    #--END
    return df


def tidy_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Turn 'Order Date' into 'order_date' so columns are easy to type."""
    #--SOLUTION:lower-case the columns, strip spaces, replace ' ' and '-' with '_'
    df.columns = (
        df.columns.str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("-", "_")
    )
    #--END
    return df


def parse_dates(df: pd.DataFrame) -> pd.DataFrame:
    """The dates arrive as text like '11/8/2023' — make them real dates."""
    #--SOLUTION:pd.to_datetime on order_date and ship_date with format="%m/%d/%Y"
    df["order_date"] = pd.to_datetime(df["order_date"], format="%m/%d/%Y")
    df["ship_date"] = pd.to_datetime(df["ship_date"], format="%m/%d/%Y")
    #--END
    return df


def drop_unneeded(df: pd.DataFrame) -> pd.DataFrame:
    """row_id is just a counter and country is always 'United States'."""
    #--SOLUTION:drop columns row_id and country (use errors="ignore")
    df = df.drop(columns=["row_id", "country"], errors="ignore")
    #--END
    return df


def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    #--SOLUTION:drop exact duplicate rows
    df = df.drop_duplicates()
    #--END
    return df


def fix_missing(df: pd.DataFrame) -> pd.DataFrame:
    """Some rows (Burlington, Vermont) have no postal_code."""
    #--SOLUTION:fill missing postal_code with 0, then cast the column to int
    df["postal_code"] = df["postal_code"].fillna(0).astype(int)
    #--END
    return df


def main() -> None:
    df = load_raw()
    df = tidy_columns(df)
    df = parse_dates(df)
    df = drop_unneeded(df)
    df = remove_duplicates(df)
    df = fix_missing(df)

    OUT.parent.mkdir(exist_ok=True)
    df.to_csv(OUT, index=False)
    print(f"Wrote {len(df)} clean rows -> {OUT}")
    print(df.dtypes)


if __name__ == "__main__":
    main()
