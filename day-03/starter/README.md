# Day 3 — Build & Share a Dashboard 📊

You cleaned Superstore's data on Day 2. Today you turn it into an interactive
**dashboard** the whole business can use — and put it online with a public link.
All in **GitHub Codespaces**.

## 1. Get your own copy

1. Click **Use this template → Create a new repository**.
2. On *your* repo: **Code → Codespaces → Create codespace on main**.
3. Wait ~1 minute while it installs everything (pandas, plotly, streamlit…).

## 2. The data

The cleaned data from Day 2 is **already in `data/clean.csv`** — see
[`data/README.md`](data/README.md). Nothing to download.

## 3. The teaching notebook

Open `notebooks/01_teaching.ipynb` and follow along: choosing charts, plotting
with pandas/seaborn, and interactive charts with plotly.

## 4. Build the dashboard

Open `src/app.py` and fill in the `# TODO`s. It **already runs** as a basic
dashboard — you're enhancing it (a region filter, a profit KPI, a trend chart).

Run it from the terminal:

```bash
streamlit run src/app.py
```

In Codespaces a pop-up offers to open the forwarded port — click it to see your
dashboard. Edit, save, and it refreshes live.

## 5. Deploy & share

Put your dashboard online with a public link — follow [`DEPLOY.md`](DEPLOY.md).
🎉 You've gone from raw data → cleaned → a shareable dashboard.

## Stretch (if you finish early)

- Add a **category** filter alongside the region one.
- Add a **download button** so people can export the filtered data
  (`st.download_button` with `view.to_csv()`).
- Add a **profit-by-category** bar chart.
- Show a **KPI delta** (e.g. profit margin %) in the metric row.
