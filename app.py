import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from scripts.data_loader import load_running_data
from scripts.visualization import (
    plot_fastest_pace_per_shoe,
    plot_monthly_trends,
    plot_shoes_usage,
    plot_elevation_gain,
    plot_monthly_distance
)

st.title("🏃🏻‍♀️ Running Data Dashboard")

# Load data from MongoDB
try:
    df = load_running_data()
    if df is not None:
        st.subheader("📊 Monthly Trends")
        st.pyplot(plot_monthly_trends(df))  

        st.subheader("👟 Shoes Usage")
        st.pyplot(plot_shoes_usage(df))

        st.subheader("⛰️ Monthly Elevation Gain")
        st.pyplot(plot_elevation_gain(df))

        st.subheader("📍 Monthly Distance")
        st.pyplot(plot_monthly_distance(df))

        st.subheader("🚀 Fastest Pace per Shoe")
        st.pyplot(plot_fastest_pace_per_shoe(df))  

    else:
        st.warning("No running data found for 2024.")

except Exception as e:
    st.error(f"An error occurred: {e}")
