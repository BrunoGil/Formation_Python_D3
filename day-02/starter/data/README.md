# The dataset

`Sample - Superstore.csv` is **already here** — you don't need to download
anything. This page just explains where it came from.

## Where it's from: Kaggle 🏷️

[Kaggle](https://www.kaggle.com) is the largest public catalogue of datasets
(and a hub for data-science competitions) — a great first stop when you need
data to work with. This is the classic **Sample - Superstore** retail dataset:

➡️ https://www.kaggle.com/datasets/vivek468/superstore-dataset-final

## Getting data from Kaggle yourself (for later)

In a real project the data won't be handed to you — you'll fetch it. Two ways:

1. **Download in the browser** (most common): open the dataset page, sign in
   (free account), click **Download**, unzip if needed, and drag the CSV into a
   `data/` folder — exactly like this one.
2. **Kaggle API** (for automation): create an API token in your Kaggle account,
   then `pip install kaggle` and
   `kaggle datasets download -d vivek468/superstore-dataset-final`.

> 💡 Real-world quirk: this file is **Windows-encoded**, not UTF-8 — which is
> why the cleaning code reads it with `encoding="latin-1"`.
