# app/dashboard.py
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os
import matplotlib.pyplot as plt

# Load environment variables
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL, future=True)

st.set_page_config(page_title="Air Quality Dashboard", layout="wide")
st.title("🌍 Global Air Quality Dashboard")

# Load data from SQLite
with engine.connect() as conn:
    df = pd.read_sql(
        text("SELECT city, date, pm25, pm10, co, no2, so2, o3 FROM air_quality ORDER BY date DESC"), conn
    )

# ----------------------------
# City selection for comparison
# ----------------------------
cities = df['city'].unique().tolist()
selected_cities = st.sidebar.multiselect(
    "Select city/cities to compare in table", cities, default=[cities[0]])

compare_data = df[df['city'].isin(selected_cities)].sort_values('date')

st.subheader("Air Quality Data Table")
st.dataframe(compare_data)

# ----------------------------
# Single city for graphs
# ----------------------------
selected_city = st.sidebar.selectbox("Select a city for graphs", cities)
city_data = df[df['city'] == selected_city].sort_values('date')

# ----------------------------
# PM2.5 & PM10 Graph
# ----------------------------
st.subheader("PM2.5 & PM10 Levels Over Time")
fig, ax = plt.subplots(figsize=(6, 3))  # smaller figure
ax.plot(pd.to_datetime(city_data['date']),
        city_data['pm25'], label="PM2.5", marker='o')
ax.plot(pd.to_datetime(city_data['date']),
        city_data['pm10'], label="PM10", marker='o')
ax.set_xlabel("Date")
ax.set_ylabel("µg/m³")
ax.legend()
st.pyplot(fig)

# ----------------------------
# Optional Gas Graph
# ----------------------------
show_gases = st.sidebar.checkbox("Show Gas Levels Graph", value=True)

if show_gases:
    st.subheader("Gas Levels Over Time")
    fig2, ax2 = plt.subplots(figsize=(6, 3))  # smaller figure
    ax2.plot(pd.to_datetime(city_data['date']), city_data['co'], label="CO")
    ax2.plot(pd.to_datetime(city_data['date']), city_data['no2'], label="NO2")
    ax2.plot(pd.to_datetime(city_data['date']), city_data['so2'], label="SO2")
    ax2.plot(pd.to_datetime(city_data['date']), city_data['o3'], label="O3")
    ax2.set_xlabel("Date")
    ax2.set_ylabel("µg/m³ or ppb")
    # auto-scale
    ax2.set_ylim(0, max(city_data[['co', 'no2', 'so2', 'o3']].max())*1.2)
    ax2.legend()
    st.pyplot(fig2)
