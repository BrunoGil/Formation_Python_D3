# Day 2 — Your First Week at Superstore 🕵️

**The scenario:** you've just joined *Superstore* as a data analyst. Leadership
handed you a messy data export and a list of questions. Clean it, summarise it,
brief them — and then see if Python can *predict* with it. All in your own
repository, running in **GitHub Codespaces**.

## 1. Get your own copy

1. Click **Use this template → Create a new repository** (top of this repo).
2. On *your* new repo, click **Code → Codespaces → Create codespace on main**.
3. Wait ~1 minute while it installs everything (pandas, Jupyter). Done — no
   setup on your laptop.

## 2. The data

The dataset is **already in `data/`** (`Sample - Superstore.csv`) — nothing to
download. It comes from **Kaggle**, the biggest public home for datasets:
[kaggle.com/datasets/vivek468/superstore-dataset-final](https://www.kaggle.com/datasets/vivek468/superstore-dataset-final).
In a real project you'd fetch data from a source like this yourself — see
[`data/README.md`](data/README.md) for how. Today it's bundled so you can dive in.

## 3. The teaching notebook

Open `notebooks/01_teaching.ipynb` and follow along with the trainer. It covers
everything you need for the exercise.

## 4. The exercise

Work through the scripts in `src/`, filling in each `# TODO`. Run each one in
the terminal as you go.

| Step | Run | What you do |
|------|-----|-------------|
| 0 | `python src/explore.py` | Look at the raw data (nothing to fill in). |
| 1 | `python src/clean.py` | Fix encoding, dates, columns, duplicates, missing values → `output/clean.csv`. |
| 2 | `python src/transform.py` | Add columns, group & summarise → `output/summary_*.csv`. |
| 3 | `python src/questions.py` | Answer leadership's questions with code. |

Each `# TODO` has a one-line hint. Stuck? Ask — that's what the trainer is for.

### 🎁 Bonus — see it & predict it

Open `notebooks/02_predict.ipynb` and run it. You'll **chart** your cleaned data
and build two tiny **machine-learning** models to predict order profit — a fun
taste of where Python can take you. (`matplotlib` and `scikit-learn` are already
installed by the devcontainer.)

## 5. Ship it

When your scripts run, commit your results:

```bash
git add output/
git commit -m "Add cleaned Superstore data and summaries"
git push
```

🎉 You've built a small, reproducible cleaning pipeline.

## Stretch (if you finish early)

- In `transform.py`, add a `summary_segment.csv`: total sales per `segment`.
- Find the `category` with the **worst average profit margin**.
- How many orders shipped the **same day** they were ordered? (`shipping_days == 0`)
- Add a `region` filter to `questions.py` and re-answer Q2 for the **West** only.
