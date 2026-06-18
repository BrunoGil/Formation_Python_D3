"""Step 3 — Answer business questions with code.

Fill in each `# TODO`, then run:

    python src/questions.py

Reads output/clean.csv (run clean.py first). Each answer is one or two lines
of pandas — use what you practised in transform.py.
"""
from pathlib import Path

import pandas as pd

CLEAN = Path("output/clean.csv")


def main() -> None:
    if not CLEAN.exists():
        raise SystemExit("output/clean.csv not found — run `python src/clean.py` first.")
    df = pd.read_csv(CLEAN, parse_dates=["order_date", "ship_date"])
    df["shipping_days"] = (df["ship_date"] - df["order_date"]).dt.days

    # Q1: Which region has the highest total profit?
    # TODO: groupby region, sum profit, .idxmax()
    print("Q1 — most profitable region:", q1)

    # Q2: Which sub_category has the LOWEST total profit (maybe even a loss)?
    # TODO: groupby sub_category, sum profit, .idxmin()
    print("Q2 — least profitable sub-category:", q2)

    # Q3: What is the average shipping time (days) per ship_mode?
    # TODO: groupby ship_mode, mean of shipping_days
    print("Q3 — average shipping days by mode:")
    print(q3)

    # Q4: Which customer segment generates the most sales?
    # TODO: groupby segment, sum sales, .idxmax()
    print("Q4 — top segment by sales:", q4)

    # Q5: Which month (1-12) had the highest total sales?
    # TODO: groupby order_date.dt.month, sum sales, .idxmax(); wrap in int() for a clean month number
    print("Q5 — best sales month:", q5)


if __name__ == "__main__":
    main()
