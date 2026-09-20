# Ford GoBike — Data Analysis Final Project

This bundle covers all three parts of the assignment.

## Part 1 — PostgreSQL (`schema.sql`, `db_interface.py`)

1. Create a database and run the schema:
   ```bash
   createdb fordgobike
   psql -d fordgobike -f schema.sql
   ```
   This creates the star schema (`fact_trips` + `dim_time`, `dim_station`, `dim_user`)
   with primary/foreign keys and `CHECK` constraints, and inserts 5 sample rows per table.

2. Launch the browser/insert interface (built with **Streamlit** rather than Qt5, since it's
   easier to run, share, and grade — the same idea as the desktop tool from the session, just
   web-based):
   ```bash
   pip install streamlit sqlalchemy psycopg2-binary pandas
   export PGHOST=localhost PGDATABASE=fordgobike PGUSER=postgres PGPASSWORD=postgres
   streamlit run db_interface.py
   ```
   It lets you browse each table and insert new rows through a form.

## Part 2 — Preprocessing & EDA (`part2_preprocessing_eda.ipynb`)

Open in Jupyter and run top to bottom (already executed once against
`fordgobike-tripdataFor201902.csv`, included here). It:
- Cleans missing values, standardizes categories, removes duration/age outliers.
- Engineers `duration_min`, a simulated `sim_date` / `sim_day_of_week` / `sim_is_weekend`
  (see the data-quality note inside the notebook — the source file's timestamps were
  truncated to `mm:ss`, with no date), and `age_group`.
- Encodes categoricals and scales numeric columns.
- Produces the EDA plots (weekday, duration distribution, subscriber vs. customer, age,
  gender, top stations), each with an analyst-style write-up.
- Exports **`fordgobike_clean.csv`**, which Part 3 uses.

## Part 3 — Interactive Dashboard (`dashboard.py`)

```bash
pip install streamlit plotly pandas
streamlit run dashboard.py
```
Loads `fordgobike_clean.csv` and gives you:
- **Sidebar filters**: date range, user type, gender, age group.
- **Overview KPIs**: total trips, avg. duration, active bikes, most popular station.
- **Time Analysis**: trips by weekday, trips across the month.
- **User Analysis**: subscriber vs. customer, gender, age group.
- **Station/Trip Analysis**: top 10 stations, duration distribution.

A live, click-around preview of the same layout (built as a standalone HTML page with a
9,000-trip sample) is also included as `ford_gobike_dashboard.html` — open it directly in a
browser, no installation needed, to see the look and feel before running the full Streamlit app.
