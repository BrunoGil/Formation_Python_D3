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
    # find data/clean.csv whether run from the repo root or src/
    path = next(p for p in [Path("data/clean.csv"), Path("../data/clean.csv")] if p.exists())
    return pd.read_csv(path, parse_dates=["order_date", "ship_date"])


df = load_data()

st.title("📊 Superstore Sales Dashboard")

# ---------------- Sidebar filter ----------------
st.sidebar.header("Filters")
regions = sorted(df["region"].unique())

chosen = regions  # default: all regions (replace via the TODO below)
#--SOLUTION:make a sidebar multiselect labelled "Region" (options=regions, default=regions), assign to `chosen`
chosen = st.sidebar.multiselect("Region", regions, default=regions)
#--END

view = df[df["region"].isin(chosen)]

if view.empty:
    st.warning("Pick at least one region to see the dashboard.")
    st.stop()

# ---------------- KPI row ----------------
c1, c2, c3 = st.columns(3)
c1.metric("Total sales", f"${view['sales'].sum():,.0f}")
#--SOLUTION:add a "Total profit" metric in column c2, formatted like total sales
c2.metric("Total profit", f"${view['profit'].sum():,.0f}")
#--END
c3.metric("Orders", f"{view['order_id'].nunique():,}", help="Unique orders (not line items)")

# ---------------- Charts ----------------
st.subheader("Sales by region")
by_region = view.groupby("region")["sales"].sum().reset_index()
st.plotly_chart(px.bar(by_region, x="region", y="sales"), use_container_width=True)

#--SOLUTION:add a "Sales over time" line chart of monthly sales (group order_date by month, sum sales)
st.subheader("Sales over time")
monthly = (
    view.groupby(view["order_date"].dt.to_period("M").dt.to_timestamp())["sales"]
    .sum()
    .reset_index()
)
st.plotly_chart(px.line(monthly, x="order_date", y="sales"), use_container_width=True)
#--END

st.subheader("Top 10 products by sales")
top = (
    view.groupby("product_name")["sales"].sum().sort_values(ascending=False).head(10).reset_index()
)
st.plotly_chart(px.bar(top, x="sales", y="product_name", orientation="h"), use_container_width=True)
