"""Generate the synthetic retail sales dataset used throughout the training.

Run from the day-01 folder:

    python generate_data.py

Produces, in ./data:
    - retail_sales.csv
    - retail_sales.xlsx

The data is deterministic (fixed seed) so everyone gets the same numbers.
A few *mild* quirks are baked in on purpose (a handful of missing values and
inconsistent category casing) so that Day 2 (cleaning) has something to work
on. Day 1 does not dwell on them.
"""

from __future__ import annotations

import random
from datetime import date, timedelta
from pathlib import Path

import pandas as pd

SEED = 42
N_ROWS = 1000
START_DATE = date(2024, 1, 1)
DAYS = 365

REGIONS = ["Norte", "Centro", "Lisboa", "Alentejo", "Algarve"]

# A store belongs to exactly one region.
STORES = {
    "Porto-01": "Norte",
    "Braga-02": "Norte",
    "Coimbra-03": "Centro",
    "Aveiro-04": "Centro",
    "Lisboa-05": "Lisboa",
    "Sintra-06": "Lisboa",
    "Evora-07": "Alentejo",
    "Faro-08": "Algarve",
}

# product -> (category, base unit price in EUR)
PRODUCTS = {
    "Whole Milk 1L": ("Dairy", 0.89),
    "Greek Yogurt 500g": ("Dairy", 1.49),
    "Sourdough Bread": ("Bakery", 1.99),
    "Croissant": ("Bakery", 0.79),
    "Bananas 1kg": ("Produce", 1.19),
    "Tomatoes 1kg": ("Produce", 1.59),
    "Sparkling Water 1.5L": ("Beverages", 0.55),
    "Orange Juice 1L": ("Beverages", 1.29),
    "Frozen Pizza": ("Frozen", 2.99),
    "Ice Cream 1L": ("Frozen", 3.49),
    "Dish Soap": ("Household", 1.79),
    "Paper Towels 4pk": ("Household", 2.29),
}


def build_dataframe() -> pd.DataFrame:
    rng = random.Random(SEED)
    product_names = list(PRODUCTS.keys())
    store_names = list(STORES.keys())

    rows = []
    for i in range(N_ROWS):
        sale_date = START_DATE + timedelta(days=rng.randint(0, DAYS - 1))
        store = rng.choice(store_names)
        region = STORES[store]
        product = rng.choice(product_names)
        category, base_price = PRODUCTS[product]

        units = rng.randint(1, 40)
        # nudge price a little around the base so it's not perfectly uniform
        unit_price = round(base_price * rng.uniform(0.95, 1.10), 2)
        revenue = round(units * unit_price, 2)

        rows.append(
            {
                "order_id": 100000 + i,
                "date": sale_date.isoformat(),
                "store": store,
                "region": region,
                "product": product,
                "category": category,
                "units_sold": units,
                "unit_price": unit_price,
                "revenue": revenue,
            }
        )

    df = pd.DataFrame(rows)

    # --- intentional, mild quirks for Day 2 (cleaning) ---
    rng_q = random.Random(SEED + 1)

    # 1) inconsistent category casing on a slice of rows
    idx_case = rng_q.sample(range(N_ROWS), k=40)
    df.loc[idx_case, "category"] = df.loc[idx_case, "category"].str.upper()

    # 2) a few missing units_sold values
    idx_missing = rng_q.sample(range(N_ROWS), k=12)
    df.loc[idx_missing, "units_sold"] = None

    # 3) a couple of duplicated rows
    dupes = df.iloc[rng_q.sample(range(N_ROWS), k=5)].copy()
    df = pd.concat([df, dupes], ignore_index=True)

    return df


def main() -> None:
    out_dir = Path(__file__).parent / "data"
    out_dir.mkdir(exist_ok=True)

    df = build_dataframe()

    csv_path = out_dir / "retail_sales.csv"
    xlsx_path = out_dir / "retail_sales.xlsx"

    df.to_csv(csv_path, index=False)
    df.to_excel(xlsx_path, index=False, sheet_name="sales")

    print(f"Wrote {len(df)} rows")
    print(f"  {csv_path}")
    print(f"  {xlsx_path}")


if __name__ == "__main__":
    main()
