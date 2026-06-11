# Day 1 data

The retail sales dataset used throughout the training.

| File | Use |
|------|-----|
| `retail_sales.csv` | CSV import block (4a) and the exercises |
| `retail_sales.xlsx` | Excel import block (4b), sheet tab named `sales` |

Regenerate both with `python ../generate_data.py` (deterministic, fixed seed).

## Google Sheet (block 4c)

For the "read from a Google Sheet" part, attendees read a **shared, read-only**
Sheet — no download needed.

**Trainer setup (do this before the session):**

1. Create a new Google Sheet and import `retail_sales.csv`
   (*File → Import → Upload*).
2. **Share** it with each attendee's email as **Viewer** (read-only).
3. Copy the Sheet URL and paste it into the `SHEET_URL` placeholder in
   `01_teaching.ipynb`, block 4c.

**Attendees** then run the block 4c cell in Colab, approve the Google sign-in
pop-up, and the Sheet loads straight into a pandas DataFrame via `gspread`.
