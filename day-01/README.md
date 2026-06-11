# Day 1 — Python for Data Analytics

**Foundations + Getting Your Data In** · 3 hours · beginner Python, runs in Google Colab.

## Materials

| File | What it is |
|------|------------|
| `01_teaching.ipynb` | The code-along lesson. Run top to bottom; exercise-heavy with 🏋️ "Your turn" cells throughout. |
| `02_exercises.ipynb` | Standalone practice problems with `# TODO` gaps for attendees. |
| `02_exercises_solution.ipynb` | The same problems, solved. |
| `data/` | The retail dataset (`csv` + `xlsx`) and Google Sheet setup notes. |
| `generate_data.py` | Regenerates the dataset (deterministic). |
| `build_notebooks.py` | Regenerates the notebooks from source content. |

## Lesson flow

1. **Why Python for analytics** — where it fits next to Sheets / Excel / Power BI / SAP
2. **Python essentials** — variables, types, lists, dictionaries
3. **Intro to pandas** — the DataFrame: inspect, select, filter, aggregate
4. **Getting data in (hands-on)** — read a CSV, an Excel file, and a Google Sheet

## Before the session

1. Run `python generate_data.py` (if the data files aren't present).
2. Set up the shared Google Sheet and paste its URL into block 4c of the
   teaching notebook — see `data/README.md`.
3. Upload the three notebooks to Google Colab.

## Running / editing locally

Notebooks are designed for Colab but run locally too (the Colab-only cells —
file upload and Google Sheet auth — skip themselves automatically).

```bash
python -m venv .venv && source .venv/bin/activate
pip install pandas openpyxl nbformat
python generate_data.py
python build_notebooks.py   # only if you change build_notebooks.py
```
