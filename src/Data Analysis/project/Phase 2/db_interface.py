"""
Ford GoBike Database Interface  —  Part 1 (PostgreSQL front-end)
-----------------------------------------------------------------
A Streamlit app that connects to the PostgreSQL star-schema database
created by schema.sql, and lets you browse / filter / insert rows
in each table (dim_time, dim_station, dim_user, fact_trips).

Run:
    pip install streamlit sqlalchemy psycopg2-binary pandas
    streamlit run db_interface.py

Before running, set your connection details either via environment
variables or by editing DB_CONFIG below:
    PGHOST, PGPORT, PGDATABASE, PGUSER, PGPASSWORD
"""

import os
import pandas as pd
import streamlit as st
from sqlalchemy import create_engine, text

st.set_page_config(page_title="Ford GoBike DB Console", layout="wide")

# ------------------------------------------------------------------
# Connection
# ------------------------------------------------------------------
DB_CONFIG = {
    "host": os.environ.get("PGHOST", "localhost"),
    "port": os.environ.get("PGPORT", "5432"),
    "dbname": os.environ.get("PGDATABASE", "fordgobike"),
    "user": os.environ.get("PGUSER", "postgres"),
    "password": os.environ.get("PGPASSWORD", "postgres"),
}


@st.cache_resource
def get_engine():
    url = (
        f"postgresql+psycopg2://{DB_CONFIG['user']}:{DB_CONFIG['password']}"
        f"@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['dbname']}"
    )
    return create_engine(url)


def run_query(sql, params=None):
    with get_engine().connect() as conn:
        return pd.read_sql(text(sql), conn, params=params)


def run_statement(sql, params=None):
    with get_engine().begin() as conn:
        conn.execute(text(sql), params or {})


# ------------------------------------------------------------------
# Sidebar navigation
# ------------------------------------------------------------------
st.sidebar.title("🚲 Ford GoBike DB Console")
table = st.sidebar.radio(
    "Choose a table",
    ["fact_trips", "dim_time", "dim_station", "dim_user"],
)
st.sidebar.markdown("---")
st.sidebar.caption(
    f"Connected to `{DB_CONFIG['dbname']}` @ {DB_CONFIG['host']}:{DB_CONFIG['port']}"
)

st.title("Ford GoBike — Database Console")
st.caption("Browse and insert rows in the star-schema PostgreSQL database (Part 1).")

tab_browse, tab_insert = st.tabs(["📋 Browse / Filter", "➕ Insert Row"])

# ------------------------------------------------------------------
# Browse tab
# ------------------------------------------------------------------
with tab_browse:
    limit = st.slider("Rows to show", 5, 200, 25)
    try:
        df = run_query(f"SELECT * FROM {table} ORDER BY 1 LIMIT :limit", {"limit": limit})
        st.dataframe(df, use_container_width=True)
        st.caption(f"{len(df)} rows shown from `{table}`.")
    except Exception as e:
        st.error(f"Could not query `{table}`. Is the database reachable? Details: {e}")

# ------------------------------------------------------------------
# Insert tab — one form per table
# ------------------------------------------------------------------
with tab_insert:
    st.subheader(f"Insert a new row into `{table}`")

    if table == "dim_time":
        with st.form("insert_dim_time"):
            date = st.date_input("Date")
            hour = st.number_input("Hour", 0, 23, 12)
            day = st.number_input("Day", 1, 31, 1)
            day_of_week = st.selectbox(
                "Day of week",
                ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
            )
            month = st.number_input("Month", 1, 12, 1)
            year = st.number_input("Year", 2000, 2100, 2019)
            if st.form_submit_button("Insert"):
                run_statement(
                    """INSERT INTO dim_time (date, hour, day, day_of_week, month, year)
                       VALUES (:date, :hour, :day, :dow, :month, :year)""",
                    {"date": date, "hour": hour, "day": day, "dow": day_of_week,
                     "month": month, "year": year},
                )
                st.success("Row inserted into dim_time.")

    elif table == "dim_station":
        with st.form("insert_dim_station"):
            name = st.text_input("Station name")
            lat = st.number_input("Latitude", format="%.6f")
            lon = st.number_input("Longitude", format="%.6f")
            if st.form_submit_button("Insert"):
                run_statement(
                    """INSERT INTO dim_station (station_name, latitude, longitude)
                       VALUES (:name, :lat, :lon)""",
                    {"name": name, "lat": lat, "lon": lon},
                )
                st.success("Row inserted into dim_station.")

    elif table == "dim_user":
        with st.form("insert_dim_user"):
            birth_year = st.number_input("Birth year", 1900, 2020, 1990)
            age = st.number_input("Age", 0, 120, 30)
            gender = st.selectbox("Gender", ["Male", "Female", "Other"])
            user_type = st.selectbox("User type", ["Subscriber", "Customer"])
            if st.form_submit_button("Insert"):
                run_statement(
                    """INSERT INTO dim_user (birth_year, age, gender, user_type)
                       VALUES (:by, :age, :gender, :utype)""",
                    {"by": birth_year, "age": age, "gender": gender, "utype": user_type},
                )
                st.success("Row inserted into dim_user.")

    elif table == "fact_trips":
        with st.form("insert_fact_trips"):
            start_time = st.text_input("Start time (YYYY-MM-DD HH:MM:SS)")
            end_time = st.text_input("End time (YYYY-MM-DD HH:MM:SS)")
            duration_sec = st.number_input("Duration (sec)", 1, step=1)
            bike_id = st.number_input("Bike ID", 1, step=1)
            start_station_id = st.number_input("Start station ID", 1, step=1)
            end_station_id = st.number_input("End station ID", 1, step=1)
            user_id = st.number_input("User ID", 1, step=1)
            time_id = st.number_input("Time ID", 1, step=1)
            if st.form_submit_button("Insert"):
                run_statement(
                    """INSERT INTO fact_trips (start_time, end_time, duration_sec, bike_id,
                                                start_station_id, end_station_id, user_id, time_id)
                       VALUES (:st, :et, :dur, :bike, :sst, :est, :uid, :tid)""",
                    {"st": start_time, "et": end_time, "dur": duration_sec, "bike": bike_id,
                     "sst": start_station_id, "est": end_station_id, "uid": user_id, "tid": time_id},
                )
                st.success("Row inserted into fact_trips.")
