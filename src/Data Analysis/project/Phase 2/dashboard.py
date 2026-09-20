"""
Ford GoBike Interactive Dashboard — Part 3
--------------------------------------------
Streamlit dashboard built on top of the cleaned dataset produced by
part2_preprocessing_eda.ipynb (fordgobike_clean.csv).

Run:
    pip install streamlit pandas plotly
    streamlit run dashboard.py
"""

import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Ford GoBike Dashboard", layout="wide")

# ------------------------------------------------------------------
# Load data
# ------------------------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("fordgobike_clean.csv", parse_dates=["sim_date"])
    return df

df = load_data()

# ------------------------------------------------------------------
# Sidebar filters
# ------------------------------------------------------------------
st.sidebar.title("Filters")

date_min, date_max = df["sim_date"].min(), df["sim_date"].max()
date_range = st.sidebar.date_input(
    "Date range", value=(date_min, date_max), min_value=date_min, max_value=date_max
)

user_types = st.sidebar.multiselect(
    "User type", options=sorted(df["user_type"].unique()), default=list(df["user_type"].unique())
)
genders = st.sidebar.multiselect(
    "Gender", options=sorted(df["member_gender"].unique()), default=list(df["member_gender"].unique())
)
age_groups = st.sidebar.multiselect(
    "Age group",
    options=["<25", "25-34", "35-44", "45-54", "55+"],
    default=["<25", "25-34", "35-44", "45-54", "55+"],
)

if isinstance(date_range, tuple) and len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date, end_date = date_min, date_max

mask = (
    (df["sim_date"] >= pd.Timestamp(start_date))
    & (df["sim_date"] <= pd.Timestamp(end_date))
    & (df["user_type"].isin(user_types))
    & (df["member_gender"].isin(genders))
    & (df["age_group"].isin(age_groups))
)
fdf = df[mask]

st.sidebar.markdown("---")
st.sidebar.caption(f"{len(fdf):,} of {len(df):,} trips match the current filters.")

# ------------------------------------------------------------------
# Header + KPIs (Section 1: Overview KPIs)
# ------------------------------------------------------------------
st.title("🚲 Ford GoBike Interactive Dashboard")
st.caption("San Francisco Bay Area · February 2019 (simulated calendar — see notebook for details)")

k1, k2, k3, k4 = st.columns(4)
k1.metric("Total trips", f"{len(fdf):,}")
k2.metric("Avg. duration", f"{fdf['duration_min'].mean():.1f} min" if len(fdf) else "–")
k3.metric("Active bikes", f"{fdf['bike_id'].nunique():,}")
top_station = fdf["start_station_name"].value_counts().idxmax() if len(fdf) else "–"
k4.metric("Most popular station", top_station)

st.markdown("---")

# ------------------------------------------------------------------
# Section 2: Time Analysis
# ------------------------------------------------------------------
st.header("📅 Time Analysis")
c1, c2 = st.columns(2)

with c1:
    weekday_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    wk = fdf["sim_day_of_week"].value_counts().reindex(weekday_order).fillna(0)
    fig = px.bar(x=wk.index, y=wk.values, labels={"x": "Day of week", "y": "Trips"},
                 title="Trips per day of week")
    st.plotly_chart(fig, use_container_width=True)

with c2:
    daily = fdf.groupby(fdf["sim_date"].dt.date).size()
    fig = px.line(x=daily.index, y=daily.values, labels={"x": "Date", "y": "Trips"},
                  title="Trips across February")
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ------------------------------------------------------------------
# Section 3: User Analysis
# ------------------------------------------------------------------
st.header("👤 User Analysis")
c1, c2, c3 = st.columns(3)

with c1:
    ut = fdf["user_type"].value_counts()
    fig = px.pie(names=ut.index, values=ut.values, hole=0.55, title="Subscriber vs. Customer")
    st.plotly_chart(fig, use_container_width=True)

with c2:
    g = fdf["member_gender"].value_counts()
    fig = px.bar(x=g.values, y=g.index, orientation="h", labels={"x": "Trips", "y": "Gender"},
                 title="Gender")
    st.plotly_chart(fig, use_container_width=True)

with c3:
    order = ["<25", "25-34", "35-44", "45-54", "55+"]
    a = fdf["age_group"].value_counts().reindex(order).fillna(0)
    fig = px.bar(x=a.index, y=a.values, labels={"x": "Age group", "y": "Trips"}, title="Age group")
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ------------------------------------------------------------------
# Section 4: Station / Trip Analysis
# ------------------------------------------------------------------
st.header("🗺️ Station & Trip Analysis")
c1, c2 = st.columns(2)

with c1:
    top_start = fdf["start_station_name"].value_counts().head(10)
    fig = px.bar(x=top_start.values, y=top_start.index, orientation="h",
                 labels={"x": "Trips", "y": ""}, title="Top 10 start stations")
    fig.update_layout(yaxis=dict(autorange="reversed"))
    st.plotly_chart(fig, use_container_width=True)

with c2:
    fig = px.histogram(fdf[fdf["duration_min"] <= fdf["duration_min"].quantile(0.99)],
                        x="duration_min", nbins=40, title="Trip duration distribution (minutes)")
    st.plotly_chart(fig, use_container_width=True)

st.caption(
    "Data cleaned & engineered in part2_preprocessing_eda.ipynb — outliers removed, "
    "missing values imputed, and day-of-week is a simulated calendar (see notebook note)."
)
