"""Build the Day 3 starter (gapped Streamlit app + teaching notebook) and the
solution app, from a single source of truth in ./_src.

    python build.py

Outputs:
    starter/src/app.py                 # gapped Streamlit dashboard
    starter/notebooks/01_teaching.ipynb
    solution/app_solution.py           # complete, for the solutions branch

Sentinels in ./_src work like Day 2:
    #--SOLUTION:<hint>
    <answer lines>
    #--END
The starter gets `# TODO: <hint>`; the solution keeps the answer lines.
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


def split_source(text: str) -> tuple[str, str]:
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
    starter_text, solution_text = split_source((SRC / "app.py").read_text())
    (STARTER_SRC / "app.py").write_text(starter_text)
    (SOLUTION / "app_solution.py").write_text(solution_text)
    print(f"  wrote {STARTER_SRC / 'app.py'} (gapped) + {SOLUTION / 'app_solution.py'}")


def md(text: str):
    return new_markdown_cell(text.strip("\n"))


def code(src: str):
    return new_code_cell(src.strip("\n"))


def build_notebook() -> None:
    cells = []
    C = cells.append

    C(md("""
# Day 3 — Visualizing & Reporting
### Python for Data Analytics

You cleaned the data on Day 2. Today you make it **talk**: pick the right chart,
plot it three ways, then build an interactive **dashboard** you can share.

**Agenda**
1. Choosing the right chart
2. Plotting basics — pandas & matplotlib, then seaborn
3. Interactive charts — plotly
4. The project — build & deploy a Streamlit dashboard

Run cells with **Shift + Enter**. 🏋️ **Your turn** cells are for you.
"""))

    C(code("""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from pathlib import Path

# the cleaned Superstore data from Day 2 (already bundled in data/)
path = next(p for p in [Path("data/clean.csv"), Path("../data/clean.csv")] if p.exists())
df = pd.read_csv(path, parse_dates=["order_date", "ship_date"])
df.head()
"""))

    # ---- Block 1 ----
    C(md("""
---
## Block 1 — Choosing the right chart

Pick the chart from the **question**, not the other way round:

| Question | Chart |
|----------|-------|
| Compare a number across categories | **Bar** |
| How does it change over time? | **Line** |
| Relationship between two numbers? | **Scatter** |
| How is one number spread out? | **Histogram** |

A chart that answers the question in two seconds beats a pretty one that doesn't.

💬 **Quick poll for the room:** "How did our sales change over the year?" — which
chart? "Which region sells most?" — which chart? Get them committing to an
answer before you scroll on.
"""))

    # ---- Block 2 ----
    C(md("""
---
## Block 2 — Plotting basics

The quickest chart is `.plot()` straight on a pandas result.
"""))

    C(code("""
# Bar: total sales per region.
df.groupby("region")["sales"].sum().plot(kind="bar", title="Sales by region")
"""))

    C(code("""
# Histogram: how are order sales spread out? (most are small, a few huge)
df["sales"].plot(kind="hist", bins=40, title="Distribution of sales")
"""))

    C(md("""
🏋️ **Your turn.** Make a **bar** chart of total **profit** per `category`.
(Hint: `df.groupby("category")["profit"].sum().plot(kind="bar")`.)
"""))

    C(code("""
# TODO: bar chart of total profit per category

"""))

    C(md("""
### seaborn — nicer statistical charts

seaborn works straight from the DataFrame and styles things for you.
"""))

    C(code("""
sns.barplot(data=df, x="region", y="sales", estimator=sum, errorbar=None)
plt.title("Total sales by region")
"""))

    C(code("""
# Scatter: is there a relationship between discount and profit?
sns.scatterplot(data=df.sample(800, random_state=0), x="discount", y="profit")
plt.title("Discount vs profit")
"""))

    C(md("""
💡 Notice high discounts drag profit negative — a real insight you can *see*.

🏋️ **Your turn.** Use `sns.boxplot` to show `profit` by `category`.
(Hint: `sns.boxplot(data=df, x="category", y="profit")`.)
"""))

    C(code("""
# TODO: boxplot of profit by category

"""))

    C(md("""
### A heatmap — two dimensions at once

A `pivot_table` summarises by **two** categories at once (region × category); a
seaborn **heatmap** colours the grid so the hot/cold spots jump out.
"""))

    C(code("""
pivot = df.pivot_table(values="sales", index="region", columns="category", aggfunc="sum")
sns.heatmap(pivot, annot=True, fmt=".0f", cmap="Blues")
plt.title("Sales by region and category")
"""))

    C(md("""
🏋️ **Your turn.** Make the same heatmap but for **profit** instead of sales.
(Hint: change `values="profit"`.)
"""))

    C(code("""
# TODO: heatmap of profit by region and category

"""))

    C(md("""
### 🔎 A real insight — predict first!

🤔 **Predict before you run the next cell:** which product **sub-category** do
you think actually *loses* money? Everyone jot a guess.
"""))

    C(code("""
df.groupby("sub_category")["profit"].sum().sort_values().plot(
    kind="barh", figsize=(7, 5), title="Total profit by sub-category")
"""))

    C(md("""
💬 **Discuss:** several sub-categories are in the **red**. *Tables* sells a lot
but **loses money** (it gets discounted hard). A chart surfaces this in seconds;
a spreadsheet hides it. Ask the room: *would you keep selling Tables?* This is
the moment they realise charts aren't decoration — they drive decisions.
"""))

    # ---- Block 3 ----
    C(md("""
---
## Block 3 — Interactive charts with plotly

Same charts, but you can **hover, zoom and pan** — and they drop straight into a
dashboard. `plotly.express` (as `px`) is the one-liner version.
"""))

    C(code("""
by_region = df.groupby("region")["sales"].sum().reset_index()
px.bar(by_region, x="region", y="sales", title="Sales by region")
"""))

    C(code("""
# Monthly sales trend.
monthly = df.groupby(df["order_date"].dt.to_period("M").dt.to_timestamp())["sales"].sum().reset_index()
px.line(monthly, x="order_date", y="sales", title="Sales over time")
"""))

    C(code("""
# Hover over points to see the product name.
px.scatter(df.sample(1000, random_state=0), x="sales", y="profit",
           color="category", hover_data=["product_name"], title="Sales vs profit")
"""))

    C(md("""
### Grouped bars — compare across two categories

`color=` plus `barmode="group"` splits each region's bar by category — great for
side-by-side comparison.
"""))

    C(code("""
grouped = df.groupby(["region", "category"])["sales"].sum().reset_index()
px.bar(grouped, x="region", y="sales", color="category", barmode="group",
       title="Sales by region and category")
"""))

    C(md("""
🏋️ **Your turn.** Make a plotly **bar** of total `sales` per `segment`.
(Hint: build a small grouped DataFrame with `.reset_index()`, then `px.bar(...)`.)
"""))

    C(code("""
# TODO: plotly bar of sales per segment

"""))

    # ---- Block 3.5: interactivity ----
    C(md("""
---
## Block 3½ — Make it interactive 🎛️

Charts get *fun* when **you** control them. `ipywidgets` adds dropdowns and
sliders that redraw a chart instantly — no server, just the notebook.

Run the next cell, then **drag the slider / change the dropdown** and watch.
"""))

    C(code("""
from ipywidgets import interact

@interact(category=["All"] + sorted(df["category"].unique()))
def sales_by_region(category="All"):
    d = df if category == "All" else df[df["category"] == category]
    d.groupby("region")["sales"].sum().plot(kind="bar", title=f"Sales by region — {category}")
"""))

    C(code("""
@interact(n=(3, 15))
def top_products(n=5):
    (df.groupby("product_name")["sales"].sum()
       .sort_values(ascending=False).head(n)
       .plot(kind="barh", title=f"Top {n} products by sales"))
"""))

    C(code("""
@interact(region=["All"] + sorted(df["region"].unique()))
def monthly_trend(region="All"):
    d = df if region == "All" else df[df["region"] == region]
    (d.groupby(d["order_date"].dt.to_period("M").dt.to_timestamp())["sales"]
       .sum().plot(marker="o", title=f"Monthly sales — {region}"))
"""))

    C(md("""
💬 **Speaking point:** "You just built a mini interactive report in *four lines*.
Imagine handing that to your manager — except they can't run a notebook. So next
we turn this into a **real web app** anyone can open with a link: **Streamlit**."

🏋️ **Your turn.** Copy the dropdown example, but plot **profit** per `segment`
instead of sales per region.
"""))

    C(code("""
# TODO: an @interact dropdown that plots profit per segment

"""))

    # ---- Block 4 ----
    C(md("""
---
## Block 4 — The project: build & deploy a dashboard 🚀

Charts in a notebook are great for you. A **dashboard** is for everyone else —
interactive, always-on, shareable with a link.

You'll build one with **Streamlit**: plain Python that becomes a web app.

1. Open `src/app.py` and fill in the `# TODO`s (a region filter, a profit KPI, a
   trend chart). It already runs as a basic dashboard — you're enhancing it.
2. Run it: `streamlit run src/app.py` — in Codespaces, click the pop-up to open
   the forwarded port.
3. **Deploy & share** it on Streamlit Community Cloud — see `DEPLOY.md` — and
   send your live link to whoever you like.

That's the full arc: raw data → cleaned → **a dashboard the business can use**. 🎉
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
    print("Building Day 3...")
    build_scripts()
    build_notebook()
    print("Done.")


if __name__ == "__main__":
    main()
