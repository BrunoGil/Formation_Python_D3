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
2. Cleaning — missing values, types, duplicates, messy text
3. Aggregation & grouping — pivot tables in one line
4. The project — clean a real Kaggle dataset in your own repo (Codespaces)

Run each cell with **Shift + Enter**. 🏋️ **Your turn** cells are for you.
"""))

    # ----- a deliberately messy little table, reused throughout -----
    C(md("""
---
## Our messy example

Real data is never tidy. Here's a tiny table with the problems you'll meet all
the time — we'll fix each one below.
"""))

    C(code("""
import pandas as pd

raw = pd.DataFrame({
    "Order ID":   ["A-1", "A-2", "A-3", "A-3", "A-4"],
    "Category":   ["Furniture", " furniture", "OFFICE", "Office", "Technology"],
    "Sales":      ["120.5", "90", "60", "60", "45.0"],   # numbers stored as text!
    "Units":      [2, None, 1, 1, 3],                    # a missing value
    "Order Date": ["1/5/2023", "2/8/2023", "3/2/2023", "3/2/2023", "4/9/2023"],
})
raw
"""))

    C(code("""
# Always look first. What's wrong here?
raw.info()
"""))

    # ----- Block 1: select / filter / sort -----
    C(md("""
---
## Block 1 — Select, filter, sort

The everyday spreadsheet moves: pick columns, keep matching rows, order them.
"""))

    C(code("""
raw[["Order ID", "Category"]]          # pick columns
"""))

    C(code("""
raw[raw["Category"] == "Technology"]   # filter rows (like a spreadsheet filter)
"""))

    C(code("""
raw.sort_values("Order ID", ascending=False)   # sort
"""))

    C(md("""
🏋️ **Your turn.** Show only the `Order ID` and `Sales` columns, for the rows
whose `Order ID` is `"A-3"`.
"""))

    C(code("""
# TODO: filter to Order ID == "A-3", then keep only Order ID and Sales

"""))

    # ----- Block 2: cleaning -----
    C(md("""
---
## Block 2 — Cleaning

### Fixing types

`Sales` is text (`"120.5"`), so we can't do maths on it. Convert it.
"""))

    C(code("""
raw["Sales"] = pd.to_numeric(raw["Sales"])
raw["Order Date"] = pd.to_datetime(raw["Order Date"], format="%m/%d/%Y")
raw.dtypes
"""))

    C(md("""
### Missing values

`Units` has a gap. You can drop rows with gaps, or fill them.
"""))

    C(code("""
print("missing per column:")
print(raw.isna().sum())

# Fill the missing Units with 0 (a choice — sometimes dropping is better).
raw["Units"] = raw["Units"].fillna(0)
"""))

    C(md("""
### Duplicates

Rows `A-3` appear twice. Drop exact duplicates.
"""))

    C(code("""
print("duplicate rows:", raw.duplicated().sum())
raw = raw.drop_duplicates()
raw
"""))

    C(md("""
### Messy text

`Category` has `"OFFICE"`, `"Office"`, `" furniture"` — same things, written
differently. Strip spaces and standardise the case.
"""))

    C(code("""
raw["Category"] = raw["Category"].str.strip().str.title()
raw["Category"].value_counts()
"""))

    C(md("""
🏋️ **Your turn.** Imagine a column had values `["YES", "yes", " Yes "]`. Write
one line that turns all three into the same value `"Yes"`.
(Hint: `.str.strip().str.title()` on a small `pd.Series([...])`.)
"""))

    C(code("""
# TODO: normalise pd.Series(["YES", "yes", " Yes "]) to all "Yes"

"""))

    # ----- Block 3: aggregation -----
    C(md("""
---
## Block 3 — Aggregation & grouping

`groupby` is the pivot table. `value_counts` counts categories.
"""))

    C(code("""
raw.groupby("Category")["Sales"].sum()          # total sales per category
"""))

    C(code("""
# Several stats at once.
raw.groupby("Category")["Sales"].agg(["sum", "mean", "count"])
"""))

    C(md("""
🏋️ **Your turn.** Compute the **average** `Sales` per `Category`.
"""))

    C(code("""
# TODO: average Sales per Category

"""))

    # ----- Block 4: the project -----
    C(md("""
---
## Block 4 — The project (your turn, for real)

Now you'll do this on a **real dataset**, in your **own repository**, using
**GitHub Codespaces** — just like a real data project.

**The dataset:** *Sample - Superstore* on Kaggle (retail orders).
**Setup:** follow the repo's `README.md` to create your repo from the template
and open it in Codespaces, then download the CSV into `data/` (see
`data/README.md`).

Then work through, filling in the `# TODO`s:

| Step | File | What you'll do |
|------|------|----------------|
| 0 | `src/explore.py` | run it — see what's messy (nothing to fill in) |
| 1 | `src/clean.py` | encoding, dates, drop columns, duplicates, missing values |
| 2 | `src/transform.py` | new columns, group & summarise, save `summary_*.csv` |
| 3 | `src/questions.py` | answer business questions with code |

Finish by **committing your `output/` files** — you'll have shipped a small,
reproducible cleaning pipeline. 🚀
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
