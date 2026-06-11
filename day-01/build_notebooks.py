"""Build the Day 1 notebooks from plain Python content blocks.

Run from the day-01 folder (after generate_data.py):

    python build_notebooks.py

Produces:
    - 01_teaching.ipynb            (code-along lesson, exercise-heavy)
    - 02_exercises.ipynb           (practice problems with gaps to fill)
    - 02_exercises_solution.ipynb  (the same problems, solved)

We build with nbformat instead of hand-writing .ipynb JSON so the files are
always valid and the exercise/solution pair can never drift apart.
"""

from __future__ import annotations

import nbformat
from nbformat.v4 import new_code_cell, new_markdown_cell, new_notebook

# --------------------------------------------------------------------------- #
# helpers
# --------------------------------------------------------------------------- #


def md(text: str):
    return new_markdown_cell(text.strip("\n"))


def code(src: str):
    return new_code_cell(src.strip("\n"))


def write(cells, path, title):
    nb = new_notebook(cells=cells)
    nb.metadata.update(
        {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3",
            },
            "language_info": {"name": "python", "version": "3"},
            "colab": {"name": title, "provenance": []},
        }
    )
    nbformat.write(nb, path)
    print(f"  wrote {path} ({len(cells)} cells)")


# --------------------------------------------------------------------------- #
# 01_teaching.ipynb
# --------------------------------------------------------------------------- #

teaching = []
T = teaching.append

T(md("""
# Day 1 — Python for Data Analytics
### Foundations + Getting Your Data In

Welcome! Today is about getting comfortable with Python and bringing your data
into a notebook. By the end of the session you will be able to:

1. Read and write a little Python without fear
2. Use **pandas** to work with data like a spreadsheet — but more powerful
3. Load data from a **CSV**, an **Excel** file, and a **Google Sheet**

**Agenda**
1. Why Python for analytics
2. Python essentials for analysts
3. Intro to pandas
4. Hands-on: getting your data in
"""))

T(md("""
## How to use this notebook

- Run a cell with **Shift + Enter**. Run them **in order**, top to bottom.
- 🏋️ **Your turn** cells are for *you* — there's a `# TODO` to complete.
  Try it before peeking; getting it wrong is part of learning.
- 💡 Tips and 📝 notes are there to connect Python back to tools you already
  know (Excel, Google Sheets, Power BI).

Let's go.
"""))

# ----- Block 1 -----------------------------------------------------------
T(md("""
---
## Block 1 — Why Python for analytics

You already do analytics in Sheets, Excel, Power BI and SAP. So why Python?

- It handles **big and messy** data that would choke a spreadsheet.
- Every step is **written down and repeatable** — no more "which cells did I
  click last month?".
- It **connects** to your existing tools (it can read your Google Sheets and
  feed Power BI), so it *complements* them rather than replacing them.

Here's a tiny taste. Don't worry about the syntax yet — just read it.
"""))

T(code("""
import pandas as pd

# A few sales rows, built by hand just for this example.
sales = pd.DataFrame({
    "store":   ["Porto-01", "Lisboa-05", "Porto-01", "Lisboa-05"],
    "revenue": [120.50,      90.00,       60.00,      45.25],
})

# Total revenue per store — the equivalent of a pivot table, in one line.
sales.groupby("store")["revenue"].sum()
"""))

T(md("""
📝 That `groupby(...).sum()` is a pivot table. One readable line, and it will
run identically on 10 rows or 10 million. That's the promise of Python for
analytics.
"""))

# ----- Block 2 -----------------------------------------------------------
T(md("""
---
## Block 2 — Python essentials for analysts

Just enough Python to be productive. We'll cover **variables**, **types**,
**lists**, and **dictionaries** — the building blocks you'll use all day.
"""))

T(md("""
### Variables and types

A **variable** is a named box that holds a value. You create one with `=`.
"""))

T(code("""
store_name = "Porto-01"     # text          -> called a 'str' (string)
units_sold = 18             # whole number  -> called an 'int'
unit_price = 0.89           # decimal       -> called a 'float'
is_open = True              # yes/no        -> called a 'bool'

print(store_name, units_sold, unit_price, is_open)
"""))

T(code("""
# 'type()' tells you what kind of value something is.
print(type(store_name))
print(type(units_sold))
print(type(unit_price))
"""))

T(code("""
# You can compute with variables, just like spreadsheet formulas.
revenue = units_sold * unit_price
print("Revenue:", revenue)
"""))

T(md("""
🏋️ **Your turn.** Create two variables, `units` (a whole number) and `price`
(a decimal), then compute and print their `total`.
"""))

T(code("""
# TODO: create `units` and `price`, then compute `total` and print it.

"""))

T(md("""
### Lists

A **list** is an ordered collection — think of a single column in a spreadsheet.
Square brackets `[ ]`, items separated by commas.
"""))

T(code("""
regions = ["Norte", "Centro", "Lisboa", "Alentejo", "Algarve"]

print(regions)
print("How many regions?", len(regions))
print("First region:", regions[0])     # counting starts at 0!
print("Last region:", regions[-1])     # -1 means 'last'
"""))

T(code("""
# Add to a list, and loop over it.
regions.append("Madeira")

for region in regions:
    print("Region:", region)
"""))

T(md("""
🏋️ **Your turn.** Make a list called `products` with three product names,
print how many there are, and print the second one.
"""))

T(code("""
# TODO: create `products`, print its length, print the second item.

"""))

T(md("""
### Dictionaries

A **dictionary** stores **key → value** pairs, like a lookup table. Curly
braces `{ }`. Great for "the price of each product" style data.
"""))

T(code("""
prices = {
    "Whole Milk 1L": 0.89,
    "Sourdough Bread": 1.99,
    "Frozen Pizza": 2.99,
}

print("Price of milk:", prices["Whole Milk 1L"])

# Update a value, and add a new one.
prices["Frozen Pizza"] = 3.19
prices["Croissant"] = 0.79
print(prices)
"""))

T(md("""
🏋️ **Your turn.** Build a dictionary `stock` mapping two product names to the
number of units in stock, then print the stock of one of them.
"""))

T(code("""
# TODO: create `stock` and print one product's stock level.

"""))

# ----- Block 3 -----------------------------------------------------------
T(md("""
---
## Block 3 — Intro to pandas

**pandas** is the spreadsheet of Python. Its main object is the **DataFrame**:
a table with named columns and rows — exactly like a sheet tab.

We'll build a small DataFrame by hand first, then load the real retail data in
Block 4.
"""))

T(code("""
import pandas as pd

df = pd.DataFrame({
    "store":      ["Porto-01", "Lisboa-05", "Faro-08", "Porto-01"],
    "region":     ["Norte", "Lisboa", "Algarve", "Norte"],
    "units_sold": [18, 9, 22, 6],
    "unit_price": [0.89, 1.99, 0.55, 2.99],
})

df
"""))

T(md("""
### Looking at a DataFrame

These four are the first things you run on *any* new dataset.
"""))

T(code("""
print("Shape (rows, columns):", df.shape)
print("Column names:", list(df.columns))
"""))

T(code("""
df.head(2)   # first rows — use df.tail(2) for the last ones
"""))

T(code("""
df.info()    # column names, types, and how many values are non-empty
"""))

T(code("""
df.describe()  # quick statistics for the numeric columns
"""))

T(md("""
### Selecting columns and rows

Pick a column with `df["column_name"]`. Pick rows that match a condition by
putting the condition inside the brackets — this is **filtering**.
"""))

T(code("""
df["store"]            # one column
"""))

T(code("""
df[["store", "units_sold"]]   # several columns -> note the double brackets
"""))

T(code("""
# Filtering: only rows in the Norte region.
df[df["region"] == "Norte"]
"""))

T(code("""
# Create a new column from existing ones — like dragging a formula down.
df["revenue"] = df["units_sold"] * df["unit_price"]
df
"""))

T(md("""
🏋️ **Your turn.** From `df`, select only the rows where `units_sold` is greater
than 10. (Hint: copy the Norte example and change the condition.)
"""))

T(code("""
# TODO: filter df to rows where units_sold > 10

"""))

T(md("""
### Aggregating and sorting

`value_counts()` counts categories. `groupby(...)` is your pivot table.
`sort_values(...)` orders rows.
"""))

T(code("""
df["region"].value_counts()
"""))

T(code("""
# Total revenue per region (a pivot table).
df.groupby("region")["revenue"].sum()
"""))

T(code("""
# Sort rows by revenue, highest first.
df.sort_values("revenue", ascending=False)
"""))

T(md("""
🏋️ **Your turn.** Compute the **average** `unit_price` per region.
(Hint: same as the revenue example, but use `.mean()` instead of `.sum()`.)
"""))

T(code("""
# TODO: average unit_price per region

"""))

# ----- Block 4 -----------------------------------------------------------
T(md("""
---
## Block 4 — Getting your data in (hands-on)

So far we typed data by hand. Now we load the **real retail dataset** three
ways: from a **CSV**, from **Excel**, and from a **Google Sheet**.
"""))

T(md("""
### 4a. From a CSV file

📝 **In Colab:** run the cell below and upload `retail_sales.csv` when prompted.
The file then lives next to your notebook, so `pd.read_csv("retail_sales.csv")`
finds it.
"""))

T(code("""
# In Colab, this opens a file picker. (Locally it's skipped automatically.)
try:
    from google.colab import files
    files.upload()   # choose retail_sales.csv (and retail_sales.xlsx)
except ImportError:
    print("Not on Colab — assuming the data files are already alongside this notebook.")
"""))

T(code("""
import pandas as pd
from pathlib import Path

# Works whether the file sits in ./data (local) or next to the notebook (Colab).
csv_path = "data/retail_sales.csv" if Path("data/retail_sales.csv").exists() else "retail_sales.csv"

sales = pd.read_csv(csv_path)
sales.head()
"""))

T(code("""
# The same four checks from Block 3 — always look before you leap.
print(sales.shape)
sales.info()
"""))

T(md("""
🏋️ **Your turn.** Show the **last** 5 rows of `sales`, and print the list of
column names.
"""))

T(code("""
# TODO: last 5 rows, then the column names

"""))

T(md("""
### 4b. From an Excel file

Same idea, different function: `pd.read_excel`. We point it at the sheet tab
named `"sales"`.
"""))

T(code("""
xlsx_path = "data/retail_sales.xlsx" if Path("data/retail_sales.xlsx").exists() else "retail_sales.xlsx"

sales_xl = pd.read_excel(xlsx_path, sheet_name="sales")
sales_xl.head()
"""))

T(md("""
💡 CSV vs Excel: a CSV is plain text (universal, lightweight, no formatting).
Excel files can hold multiple tabs, formulas and styling. pandas reads both —
you pick the right tool for the file you were given.
"""))

T(md("""
### 4c. From a Google Sheet (Colab)

Your trainer has shared a read-only Google Sheet with your email. This is how
you pull it straight into pandas — no download step.

📝 This cell only works **in Colab** (it uses Colab's Google sign-in). Run it,
approve the access pop-up, and paste the shared sheet URL where indicated.
"""))

T(code("""
# --- Reading a Google Sheet from Colab ---
try:
    from google.colab import auth
    auth.authenticate_user()            # a pop-up asks you to sign in / allow

    import gspread
    from google.auth import default
    creds, _ = default()
    gc = gspread.authorize(creds)

    SHEET_URL = "PASTE_THE_SHARED_SHEET_URL_HERE"
    worksheet = gc.open_by_url(SHEET_URL).sheet1

    sales_gs = pd.DataFrame(worksheet.get_all_records())
    print("Loaded", sales_gs.shape[0], "rows from the Google Sheet")
    sales_gs.head()
except ImportError:
    print("This cell is for Google Colab. Run it there to read the shared Sheet.")
"""))

T(md("""
🏋️ **Your turn (in Colab).** Once `sales_gs` is loaded, print its shape and use
`value_counts()` to see how many rows each `region` has.
"""))

T(code("""
# TODO (run in Colab): sales_gs.shape, then sales_gs["region"].value_counts()

"""))

T(md("""
---
## Recap

Today you:

- Wrote variables, lists and dictionaries in Python
- Used a pandas **DataFrame** to inspect, select, filter and aggregate data
- Loaded the retail data from **CSV**, **Excel** and a **Google Sheet**

**Tomorrow (Day 2):** we clean this data — those missing values and messy
category labels you may have spotted — and reshape it for analysis.

Great work! 🎉
"""))


# --------------------------------------------------------------------------- #
# Exercises + solutions  (one source of truth -> two notebooks)
# --------------------------------------------------------------------------- #
# Each entry: (section_markdown_or_None, prompt_markdown, solution_code)

EX_INTRO = """
# Day 1 — Practice Exercises
### Python for Data Analytics

Work through these at your own pace. Each problem has a short prompt and an
empty cell with a `# TODO`. Fill it in and run it.

There is a matching **solution notebook** — try every problem first, then check.

> **Setup:** if you're on Colab, run the upload cell below and pick
> `retail_sales.csv`. Then run the import cell.
"""

EX_SETUP_CODE = """
# Colab only: upload retail_sales.csv when prompted.
try:
    from google.colab import files
    files.upload()
except ImportError:
    print("Not on Colab — assuming retail_sales.csv is alongside this notebook.")
"""

EX_IMPORT_CODE = """
import pandas as pd
from pathlib import Path

csv_path = "data/retail_sales.csv" if Path("data/retail_sales.csv").exists() else "retail_sales.csv"
sales = pd.read_csv(csv_path)
sales.head()
"""

EXERCISES = [
    (
        "## Part A — Python basics",
        "**A1.** Create a variable `vat` set to `0.23` and a variable "
        "`net_price` set to `2.00`. Compute `gross = net_price * (1 + vat)` "
        "and print it.",
        "vat = 0.23\nnet_price = 2.00\ngross = net_price * (1 + vat)\nprint(gross)",
    ),
    (
        None,
        "**A2.** Make a list `categories` with: `\"Dairy\"`, `\"Bakery\"`, "
        "`\"Frozen\"`. Print how many items it has and the **first** one.",
        'categories = ["Dairy", "Bakery", "Frozen"]\nprint(len(categories))\nprint(categories[0])',
    ),
    (
        None,
        "**A3.** Loop over `categories` and print `\"Category: X\"` for each.",
        'for c in categories:\n    print("Category:", c)',
    ),
    (
        None,
        "**A4.** Build a dictionary `prices` with `\"Milk\": 0.89` and "
        "`\"Bread\": 1.99`. Then change the price of Bread to `2.09` and print "
        "the dictionary.",
        'prices = {"Milk": 0.89, "Bread": 1.99}\nprices["Bread"] = 2.09\nprint(prices)',
    ),
    (
        "## Part B — Exploring the data\n\nMake sure you've run the setup and import cells above so `sales` exists.",
        "**B1.** Print the **shape** of `sales` (rows, columns) and the list of "
        "column names.",
        'print(sales.shape)\nprint(list(sales.columns))',
    ),
    (
        None,
        "**B2.** Show the first 10 rows.",
        "sales.head(10)",
    ),
    (
        None,
        "**B3.** Run `.info()` and `.describe()` on `sales`. How many rows have "
        "a missing `units_sold`? (Look at the non-null count.)",
        "sales.info()\nsales.describe()",
    ),
    (
        None,
        "**B4.** Select just the `product` and `revenue` columns and show the "
        "first 5 rows.",
        'sales[["product", "revenue"]].head()',
    ),
    (
        "## Part C — Filtering and aggregating",
        "**C1.** Filter `sales` to rows from the `\"Lisboa\"` region. How many "
        "rows are there?",
        'lisboa = sales[sales["region"] == "Lisboa"]\nprint(lisboa.shape[0])\nlisboa.head()',
    ),
    (
        None,
        "**C2.** Filter to rows where `units_sold` is greater than 30.",
        'sales[sales["units_sold"] > 30]',
    ),
    (
        None,
        "**C3.** Use `value_counts()` to count how many rows each `category` "
        "has. (You'll notice some odd UPPERCASE labels — that's Day 2's job!)",
        'sales["category"].value_counts()',
    ),
    (
        None,
        "**C4.** Compute the **total revenue per region** using `groupby`.",
        'sales.groupby("region")["revenue"].sum()',
    ),
    (
        None,
        "**C5.** Compute the **average `unit_price` per category**, then sort "
        "the result from highest to lowest.",
        'sales.groupby("category")["unit_price"].mean().sort_values(ascending=False)',
    ),
    (
        "## Part D — Stretch (optional)",
        "**D1.** Find the single `product` with the highest total revenue. "
        "(Hint: `groupby` the product, `.sum()` the revenue, then "
        "`.sort_values(ascending=False).head(1)`.)",
        'sales.groupby("product")["revenue"].sum().sort_values(ascending=False).head(1)',
    ),
    (
        None,
        "**D2.** Add a new column `revenue_per_unit = revenue / units_sold` and "
        "show the first few rows. (Rows with missing `units_sold` will show "
        "`NaN` — that's expected.)",
        'sales["revenue_per_unit"] = sales["revenue"] / sales["units_sold"]\nsales.head()',
    ),
]


def build_exercise_notebooks():
    ex_cells = [md(EX_INTRO), code(EX_SETUP_CODE), code(EX_IMPORT_CODE)]
    sol_cells = [
        md(EX_INTRO.replace("# Day 1 — Practice Exercises", "# Day 1 — Practice Exercises (Solutions)")),
        code(EX_SETUP_CODE),
        code(EX_IMPORT_CODE),
    ]

    for section, prompt, solution in EXERCISES:
        if section:
            ex_cells.append(md(section))
            sol_cells.append(md(section))
        ex_cells.append(md(prompt))
        ex_cells.append(code("# TODO\n"))
        sol_cells.append(md(prompt))
        sol_cells.append(code(solution))

    write(ex_cells, "02_exercises.ipynb", "Day 1 — Exercises")
    write(sol_cells, "02_exercises_solution.ipynb", "Day 1 — Exercises (Solutions)")


def main():
    print("Building notebooks...")
    write(teaching, "01_teaching.ipynb", "Day 1 — Teaching")
    build_exercise_notebooks()
    print("Done.")


if __name__ == "__main__":
    main()
