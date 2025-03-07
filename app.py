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

df = None 

st.title("🏃🏻‍♀️ Running Data Dashboard")

# Load data from MongoDB
try:
    df = load_running_data()

    if df is not None:
        df = df[df['shoes'] != 'Unknown']  # Go awayyyy unknow shoes

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

if df is not None:
    st.sidebar.title("Filters")

    # Filter shoes excluding 
    shoe_options = ["All"] + list(df['shoes'].unique())

    # Dropdown menu
    selected_shoe = st.sidebar.selectbox("Select Shoes", shoe_options, index=0)

    # Apply filter 
    if selected_shoe != "All":
        df = df[df['shoes'] == selected_shoe]
        st.write(f"✅ Filter applied: {selected_shoe}")
    else:
        st.write("✅ Showing all shoes")

else:
    st.warning("No data available.")

# Button to download data as CSV file
csv = df.to_csv(index=False)
st.download_button(label="Download Data as CSV", data=csv, file_name="running_data.csv", mime="text/csv")
