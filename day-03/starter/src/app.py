"""Superstore sales dashboard (Streamlit).

Fill in each `# TODO`, then run it:

    streamlit run src/app.py

In Codespaces a pop-up offers to open the forwarded port — click it.
"""
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Superstore Dashboard", layout="wide")


@st.cache_data
def load_data() -> pd.DataFrame:
    # Resolve data path robustly regardless of current working directory.
    # Try a few likely locations relative to the repository and this file.
    here = Path(__file__).resolve().parent
    candidates = [
        Path("data/clean.csv"),
        Path("../data/clean.csv"),
        here / "data" / "clean.csv",
        here.parent / "data" / "clean.csv",
        here.parent.parent / "data" / "clean.csv",
    ]

    for p in candidates:
        if p.exists():
            return pd.read_csv(p, parse_dates=["order_date", "ship_date"])

    tried = "\n".join(str(p) for p in candidates)
    raise FileNotFoundError(
        "Could not find data/clean.csv. Tried the following paths:\n" + tried
    )


df = load_data()

st.title("📊 Superstore Sales Dashboard")

# ---------------- Sidebar filter ----------------
st.sidebar.header("Filters")
regions = sorted(df["region"].unique())

chosen = regions  # default: all regions (replace via the TODO below)
# TODO: make a sidebar multiselect labelled "Region" (options=regions, default=regions), assign to `chosen`
chosen = st.sidebar.multiselect("Region", options=regions, default=regions)

view = df[df["region"].isin(chosen)]

if view.empty:
    st.warning("Pick at least one region to see the dashboard.")
    st.stop()

# ---------------- KPI row ----------------
c1, c2, c3 = st.columns(3)
c1.metric("Total sales", f"${view['sales'].sum():,.0f}")
c2.metric("Total profit", f"${view['profit'].sum():,.0f}")
c3.metric("Orders", f"{view['order_id'].nunique():,}", help="Unique orders (not line items)")

# ---------------- Charts ----------------
st.subheader("Sales by region")
by_region = view.groupby("region")["sales"].sum().reset_index()
st.plotly_chart(px.bar(by_region, x="region", y="sales"), use_container_width=True)

# Sales over time: group by month and produce a datetime x-axis (Plotly needs datetimes)
monthly_sales = (
    view.set_index("order_date").resample("ME")["sales"].sum().reset_index()
)

st.subheader("Sales over time")
st.plotly_chart(px.line(monthly_sales, x="order_date", y="sales", markers=True), use_container_width=True)

st.subheader("Top 10 products by sales")
top = (
    view.groupby("product_name")["sales"].sum().sort_values(ascending=False).head(10).reset_index()
)
st.plotly_chart(px.bar(top, x="sales", y="product_name", orientation="h"), use_container_width=True)
