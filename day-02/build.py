"""Build the Day 2 starter (gapped scripts + teaching notebook) and the
solution scripts, all from a single source of truth in ./_src.

Run from the day-02 folder:

    python build.py

Outputs:
    starter/src/{explore,clean,transform,questions}.py   # explore complete, rest gapped
    starter/notebooks/01_teaching.ipynb
    solution/{clean,transform,questions}_solution.py      # complete, for the solutions branch

Source scripts in ./_src mark their answers with sentinels:

    #--SOLUTION:<hint shown to attendees>
    <one or more answer lines>
    #--END

The starter gets `# TODO: <hint>` in place of the block; the solution keeps the
answer lines (sentinels stripped). So the two can never drift apart.
"""
from __future__ import annotations

from pathlib import Path

import nbformat
from nbformat.v4 import new_code_cell, new_markdown_cell, new_notebook

HERE = Path(__file__).parent
SRC = HERE / "_src"
STARTER_SRC = HERE / "starter" / "src"
NOTEBOOKS = HERE / "starter" / "notebooks"
SOLUTION = HERE / "solution"

GAPPED = ["clean.py", "transform.py", "questions.py"]  # explore.py is given complete


# --------------------------------------------------------------------------- #
# script generation (sentinel processing)
# --------------------------------------------------------------------------- #


def split_source(text: str) -> tuple[str, str]:
    """Return (starter_text, solution_text) for one source script."""
    starter, solution = [], []
    inside = False
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("#--SOLUTION:"):
            indent = line[: len(line) - len(line.lstrip())]
            hint = stripped[len("#--SOLUTION:"):].strip()
            starter.append(f"{indent}# TODO: {hint}")
            inside = True
            continue
        if stripped == "#--END":
            inside = False
            continue
        if not inside:
            starter.append(line)
        solution.append(line)
    return "\n".join(starter) + "\n", "\n".join(solution) + "\n"


def build_scripts() -> None:
    STARTER_SRC.mkdir(parents=True, exist_ok=True)
    SOLUTION.mkdir(parents=True, exist_ok=True)

    # explore.py: complete in the starter, no solution needed
    (STARTER_SRC / "explore.py").write_text((SRC / "explore.py").read_text())
    print(f"  wrote {STARTER_SRC / 'explore.py'} (complete)")

    for name in GAPPED:
        starter_text, solution_text = split_source((SRC / name).read_text())
        (STARTER_SRC / name).write_text(starter_text)
        sol_name = name.replace(".py", "_solution.py")
        (SOLUTION / sol_name).write_text(solution_text)
        print(f"  wrote {STARTER_SRC / name} (gapped) + {SOLUTION / sol_name}")


# --------------------------------------------------------------------------- #
# teaching notebook
# --------------------------------------------------------------------------- #


def md(text: str):
    return new_markdown_cell(text.strip("\n"))


def code(src: str):
    return new_code_cell(src.strip("\n"))


def build_notebook() -> None:
    cells = []
    C = cells.append

    C(md("""
# Day 2 — Manipulating & Cleaning Data
### Python for Data Analytics

Yesterday we loaded data. Today we make it **trustworthy and useful**: select
the rows we want, fix the messes real data always has, and summarise it.

**Agenda**
1. Select, filter, sort — your Sheets/Excel moves, in pandas
2. Cleaning — names, types, missing values, duplicates, messy text
3. Aggregation & grouping — pivot tables in one line
4. The project — clean a real Kaggle dataset in your own repo (Codespaces)

Run each cell with **Shift + Enter**, in order. 🏋️ **Your turn** cells are for
you to fill in.
"""))

    # ----- a deliberately messy little table, reused throughout -----
    C(md("""
---
## Our messy dataset

Real data is never tidy. Here's a small orders table with the problems you meet
all the time. We'll explore it, then fix every issue — the same arc as today's
project.
"""))

    C(code("""
import pandas as pd

raw = pd.DataFrame({
    "Order ID":   ["A-1","A-2","A-3","A-4","A-5","A-6","A-7","A-8","A-9","A-10","A-11","A-12","A-3","A-6"],
    "Region":     ["West","East","East","Central","West","Central","East","West","Central","East","West","Central","East","Central"],
    "Category":   ["Furniture"," furniture","OFFICE","Office","Technology"," technology","Furniture","Office","Technology","Office","Furniture","Technology","OFFICE"," technology"],
    "Sales":      ["120.5","90","60","45.0","300","150.75","80","200","75.25","110","95","60","60","150.75"],
    "Units":      [2, None, 1, 3, 1, 2, None, 4, 1, 2, 3, 1, 1, 2],
    "Order Date": ["1/5/2023","2/8/2023","3/2/2023","4/9/2023","5/1/2023","6/3/2023","7/7/2023","8/8/2023","9/9/2023","10/10/2023","11/11/2023","12/12/2023","3/2/2023","6/3/2023"],
})
raw
"""))

    C(md("""
The first thing you do with *any* new data: look at it. `.info()` shows the
columns, their types, and how many values are filled in.
"""))

    C(code("""
raw.info()
"""))

    C(md("""
Spot the problems already:
- `Sales` is stored as **text** (`object`), not numbers — we can't add it up yet.
- `Units` has **missing** values (fewer non-null than rows).
- `Order Date` is **text**, not a date.
- `Category` is written inconsistently (`OFFICE`, `Office`, ` furniture`).
- Some rows look **duplicated** (`A-3`, `A-6` appear twice).

🏋️ **Your turn.** Print the **shape** of `raw` (rows, columns) and the list of
its column names.
"""))

    C(code("""
# TODO: print raw.shape and list(raw.columns)

"""))

    # ----- Block 1: select / filter / sort -----
    C(md("""
---
## Block 1 — Select, filter, sort

The everyday spreadsheet moves: pick columns, keep matching rows, order them.
"""))

    C(md("""
### Selecting columns

One column (a **Series**) uses single brackets. Several columns (a
**DataFrame**) use double brackets.
"""))

    C(code("""
raw["Region"]            # one column -> a Series
"""))

    C(code("""
raw[["Order ID", "Sales"]]   # several columns -> a DataFrame (note the double [[ ]])
"""))

    C(md("""
### Filtering rows

Put a condition inside the brackets to keep only the rows where it's `True` —
just like a spreadsheet filter.
"""))

    C(code("""
raw[raw["Region"] == "West"]
"""))

    C(md("""
Combine conditions with `&` (and) / `|` (or). **Each condition needs its own
parentheses.**
"""))

    C(code("""
raw[(raw["Region"] == "West") & (raw["Category"] == "Furniture")]
"""))

    C(code("""
# Match any of several values with .isin(...)
raw[raw["Region"].isin(["West", "East"])]
"""))

    C(md("""
🏋️ **Your turn.** Keep only the rows where `Region` is `"Central"`, and show
just the `Order ID` and `Sales` columns.
"""))

    C(code("""
# TODO: filter to Region == "Central", then select Order ID and Sales

"""))

    C(md("""
### Sorting

`sort_values` orders rows. You can sort by one column or several.
"""))

    C(code("""
raw.sort_values("Order ID")
"""))

    C(code("""
# Sort by Region first, then Order ID within each region.
raw.sort_values(["Region", "Order ID"])
"""))

    C(md("""
🏋️ **Your turn.** Sort `raw` by `Region`, but in **descending** order.
(Hint: `sort_values("Region", ascending=False)`.)
"""))

    C(code("""
# TODO: sort by Region descending

"""))

    # ----- Block 2: cleaning -----
    C(md("""
---
## Block 2 — Cleaning

Now we fix the mess, one issue at a time. Each fix below is exactly what you'll
do on the real dataset in the project.
"""))

    C(md("""
### 1. Tidy the column names

`"Order ID"` is awkward to type (spaces, capitals). Standardise to `order_id`
style — lower case, no spaces.
"""))

    C(code("""
raw.columns = raw.columns.str.strip().str.lower().str.replace(" ", "_")
list(raw.columns)
"""))

    C(md("""
📝 From here on the columns are `order_id`, `region`, `category`, `sales`,
`units`, `order_date`.

### 2. Fix the types

`to_numeric` turns text into numbers; `to_datetime` turns text into real dates.
"""))

    C(code("""
raw["sales"] = pd.to_numeric(raw["sales"])
raw["order_date"] = pd.to_datetime(raw["order_date"], format="%m/%d/%Y")
raw.dtypes
"""))

    C(md("""
💡 If some values can't be converted (e.g. `"n/a"`), add `errors="coerce"` and
pandas turns the bad ones into `NaN` instead of crashing:
"""))

    C(code("""
pd.to_numeric(pd.Series(["10", "20", "n/a"]), errors="coerce")
"""))

    C(md("""
🏋️ **Your turn.** Convert this price Series to numbers, turning the bad value
into `NaN`: `pd.Series(["1.99", "3.50", "free"])`.
"""))

    C(code("""
# TODO: pd.to_numeric(..., errors="coerce")

"""))

    C(md("""
### 3. Handle missing values

See where the gaps are, then decide: **fill** them or **drop** them.
"""))

    C(code("""
raw.isna().sum()
"""))

    C(code("""
# Option A: fill the missing Units with 0.
raw["units"] = raw["units"].fillna(0)

# Option B (not used here): raw.dropna(subset=["units"]) would drop those rows.
raw["units"].isna().sum()
"""))

    C(md("""
🏋️ **Your turn.** Imagine `s = pd.Series([10, None, 30])`. Fill the missing
value with the **mean** of the series. (Hint: `s.fillna(s.mean())`.)
"""))

    C(code("""
# TODO: fill the missing value with the mean
s = pd.Series([10, None, 30])

"""))

    C(md("""
### 4. Remove duplicates

`duplicated()` flags repeated rows; `drop_duplicates()` removes them.
"""))

    C(code("""
print("duplicate rows:", raw.duplicated().sum())
raw = raw.drop_duplicates()
print("rows now:", len(raw))
"""))

    C(md("""
💡 You can also dedupe on *specific* columns: `drop_duplicates(subset=["order_id"])`
keeps one row per order id.

### 5. Clean up messy text

`category` has `"OFFICE"`, `"Office"`, `" furniture"` — the same things written
differently. Strip spaces and standardise the case.
"""))

    C(code("""
raw["category"] = raw["category"].str.strip().str.title()
raw["category"].value_counts()
"""))

    C(md("""
💡 For known one-off fixes, `replace` maps specific values to new ones, e.g.
`df["region"].replace({"W": "West", "E": "East"})`.

🏋️ **Your turn.** Normalise this Series so all three become `"Yes"`:
`pd.Series(["YES", "yes", " Yes "])`. (Hint: `.str.strip().str.title()`.)
"""))

    C(code("""
# TODO: normalise to all "Yes"

"""))

    # ----- Block 3: aggregation -----
    C(md("""
---
## Block 3 — Aggregation & grouping

Our data is clean — now we summarise it. `value_counts` counts categories;
`groupby` is the pivot table.
"""))

    C(code("""
raw["region"].value_counts()
"""))

    C(code("""
# Add normalize=True to get proportions instead of counts.
raw["region"].value_counts(normalize=True)
"""))

    C(md("""
### groupby — the pivot table

Split the data into groups, then compute something per group.
"""))

    C(code("""
raw.groupby("region")["sales"].sum()          # total sales per region
"""))

    C(code("""
# Several statistics at once.
raw.groupby("region")["sales"].agg(["sum", "mean", "count"])
"""))

    C(code("""
# Group by two columns: sales per region AND category.
raw.groupby(["region", "category"])["sales"].sum()
"""))

    C(md("""
### pivot_table — a 2-D summary

`pivot_table` lays groups out as a grid — regions down the side, categories
across the top — exactly like a spreadsheet pivot table.
"""))

    C(code("""
pd.pivot_table(raw, values="sales", index="region", columns="category",
               aggfunc="sum", fill_value=0)
"""))

    C(md("""
🏋️ **Your turn.** Compute the **average** `sales` per `category`.
(Hint: `groupby("category")` then `.mean()` on `sales`.)
"""))

    C(code("""
# TODO: average sales per category

"""))

    C(md("""
🏋️ **Your turn.** Compute the **total `units`** sold per `region`, and sort the
result from highest to lowest.
"""))

    C(code("""
# TODO: total units per region, sorted descending

"""))

    # ----- Block 4: the project -----
    C(md("""
---
## Block 4 — The project (your turn, for real)

Now you'll do all of this on a **real dataset**, in your **own repository**,
using **GitHub Codespaces** — just like a real data project.

**The dataset:** *Sample - Superstore* on Kaggle (retail orders).
**Setup:** follow the repo's `README.md` to create your repo from the template
and open it in Codespaces, then download the CSV into `data/` (see
`data/README.md`).

Then work through, filling in the `# TODO`s:

| Step | File | What you'll do |
|------|------|----------------|
| 0 | `src/explore.py` | run it — see what's messy (nothing to fill in) |
| 1 | `src/clean.py` | encoding, names, dates, drop columns, duplicates, missing values |
| 2 | `src/transform.py` | new columns, group & summarise, save `summary_*.csv` |
| 3 | `src/questions.py` | answer business questions with code |

Everything you need is in the blocks above — names, types, missing values,
duplicates, text, and `groupby`. Finish by **committing your `output/` files**:
you'll have shipped a small, reproducible cleaning pipeline. 🚀
"""))

    nb = new_notebook(cells=cells)
    nb.metadata.update(
        {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python", "version": "3"},
        }
    )
    NOTEBOOKS.mkdir(parents=True, exist_ok=True)
    out = NOTEBOOKS / "01_teaching.ipynb"
    nbformat.write(nb, out)
    print(f"  wrote {out} ({len(cells)} cells)")


def main() -> None:
    print("Building Day 2...")
    build_scripts()
    build_notebook()
    print("Done.")


if __name__ == "__main__":
    main()
