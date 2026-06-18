# Day 2 — Manipulating & Cleaning Data (trainer)

**3 hours.** A real-project experience: attendees clean the *Sample - Superstore*
Kaggle dataset in their **own repo**, running in **GitHub Codespaces** (no local
setup). Teaching notebook first, then a 3-step fill-in-the-blanks pipeline.

## Shape of the day

| Time | Block |
|------|-------|
| ~20 min | Launch Codespace from the template, download the Kaggle CSV |
| ~60 min | Teaching notebook (`01_teaching.ipynb`) — select/filter/sort, cleaning, grouping |
| ~95 min | Independent exercise — `src/clean.py` → `transform.py` → `questions.py` |
| ~15 min | Commit results, wrap-up, bridge to Day 3 (visualising the cleaned data) |

## How this folder is organised

```
day-02/
├── _src/            # SOURCE OF TRUTH — scripts with #--SOLUTION sentinels
├── build.py         # generates the starter scripts, solutions, and notebook
├── starter/         # ← becomes the attendee TEMPLATE repo (see below)
└── solution/        # generated *_solution.py (for the solutions branch)
```

Edit exercises in `_src/`, then run `python build.py` to regenerate everything.
The starter scripts get `# TODO` gaps; `solution/` gets the complete versions.

## Publishing the template repo (one-time)

1. Create a new GitHub repo (e.g. `superstore-cleanup`) from the contents of
   `starter/`.
2. In its **Settings**, tick **Template repository** so attendees can
   *Use this template*.
3. Add a `solutions` branch with the completed scripts under their
   `*_solution.py` names (from `solution/`), so a later merge keeps them
   alongside the originals without overwriting. Point attendees there after the
   session.

## Dataset

*Sample - Superstore* — https://www.kaggle.com/datasets/vivek468/superstore-dataset-final
Quirks the exercise targets: Windows (cp1252) encoding, text dates, redundant
columns, duplicate rows, missing postal codes.
