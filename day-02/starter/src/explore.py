"""Step 0 — Explore the raw data. RUN THIS FIRST (nothing to fill in).

    python src/explore.py

It prints a quick profile so you can see what needs cleaning.
"""
from pathlib import Path

import pandas as pd

RAW = Path("data/Sample - Superstore.csv")


def main() -> None:
    if not RAW.exists():
        raise SystemExit(
            f"Can't find '{RAW}'.\n"
            "Download the dataset from Kaggle and drop the CSV into data/.\n"
            "See data/README.md for the link and steps."
        )

    # NOTE: this file is Windows-encoded (cp1252 / latin-1), not UTF-8.
    df = pd.read_csv(RAW, encoding="latin-1")

    pd.set_option("display.max_columns", None)
    pd.set_option("display.width", 120)

    print("=== shape (rows, columns) ===")
    print(df.shape)
    print("\n=== columns & types ===")
    print(df.dtypes)
    print("\n=== first rows ===")
    print(df.head())
    print("\n=== missing values per column ===")
    print(df.isna().sum())
    print("\n=== duplicate rows ===")
    print(df.duplicated().sum())


if __name__ == "__main__":
    main()
