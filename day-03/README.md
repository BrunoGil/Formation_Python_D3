# Day 3 — Visualizing & Reporting (trainer)

**3 hours.** Attendees turn Day 2's cleaned data into an interactive **Streamlit
dashboard** and deploy it to a public link. Runs in **GitHub Codespaces**;
Day 2's `clean.csv` is bundled, so Day 3 doesn't depend on finishing Day 2.

## Shape of the day

| Time | Block |
|------|-------|
| ~10 min | Launch Codespace (data bundled) |
| ~55 min | Teaching notebook (`01_teaching.ipynb`) — choosing charts, pandas/seaborn, plotly |
| ~75 min | Build the dashboard (`src/app.py`, fill the `# TODO`s, run locally) |
| ~25 min | Deploy & share on Streamlit Community Cloud → public URL |
| ~15 min | Commit, wrap, course recap |

## How this folder is organised

```
day-03/
├── _src/app.py      # SOURCE OF TRUTH — Streamlit app with #--SOLUTION sentinels
├── build.py         # generates the gapped app, the solution, and the notebook
├── starter/         # ← becomes the attendee TEMPLATE repo (bundles clean.csv)
└── solution/        # generated app_solution.py (for the solutions branch)
```

Edit `_src/app.py` or `build.py`'s notebook cells, then `python build.py`.

## Deploy notes

Streamlit Community Cloud (https://share.streamlit.io) is free and deploys from a
public GitHub repo — main file path `src/app.py`. Needs a free sign-in with
GitHub. If sign-ups drag during the session, demo one deploy live and have
attendees do theirs after. See `starter/DEPLOY.md`.

## Publishing the template repo (one-time)

Same as Day 2: create a repo from `starter/`, mark it **Template repository**,
and add a `solutions` branch carrying `app_solution.py` (from `solution/`).
