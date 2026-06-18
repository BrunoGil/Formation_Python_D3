"""Step 2 — Transform & summarise the cleaned data.

Fill in each `# TODO`, then run:

    python src/transform.py

Reads output/clean.csv (run clean.py first) and writes a few summary_*.csv
files you could hand to a colleague or load into Power BI.
"""
from pathlib import Path

import pandas as pd

CLEAN = Path("output/clean.csv")
OUT_DIR = Path("output")


def load_clean() -> pd.DataFrame:
    if not CLEAN.exists():
        raise SystemExit("output/clean.csv not found — run `python src/clean.py` first.")
    return pd.read_csv(CLEAN, parse_dates=["order_date", "ship_date"])


def add_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Add two useful business metrics."""
    # TODO: add a column 'profit_margin' = profit as a fraction of sales
    # TODO: add a column 'shipping_days' = number of days between order_date and ship_date
    return df


def sales_by_region(df: pd.DataFrame) -> pd.DataFrame:
    """Total sales and profit per region, biggest sales first."""
    # TODO: groupby region, sum sales+profit, sort by sales descending; assign to `result`
    return result


def sales_by_category(df: pd.DataFrame) -> pd.Series:
    """Total sales per category and sub_category, biggest first."""
    # TODO: groupby category & sub_category, sum sales, sort descending; assign to `result`
    return result


def top_products(df: pd.DataFrame, n: int = 10) -> pd.Series:
    """The n products with the highest total sales."""
    # TODO: groupby product_name, sum sales, sort descending, take head(n); assign to `result`
    return result


def main() -> None:
    df = load_clean()
    df = add_columns(df)

    OUT_DIR.mkdir(exist_ok=True)
    sales_by_region(df).to_csv(OUT_DIR / "summary_region.csv")
    sales_by_category(df).to_csv(OUT_DIR / "summary_category.csv")
    top_products(df).to_csv(OUT_DIR / "summary_top_products.csv")

    print("Wrote summary_region.csv, summary_category.csv, summary_top_products.csv")
    print("\nSales & profit by region:")
    print(sales_by_region(df))


if __name__ == "__main__":
    main()
