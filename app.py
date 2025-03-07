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

    # Remove "Unknown" shoes from the dataframe immediately after loading
    if df is not None:
        df = df[df['shoes'] != 'Unknown']

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

    # Filter shoes excluding "Unknown" shoes
    shoe_options = ["All"] + list(df['shoes'].unique())

    # Dropdown menu
    selected_shoe = st.sidebar.selectbox("Select Shoes", shoe_options, index=0)

    # Apply filter based on selected shoe
    if selected_shoe != "All":
        df = df[df['shoes'] == selected_shoe]
        st.write(f"✅ Filter applied: {selected_shoe}")
    else:
        st.write("✅ Showing all shoes")

else:
    st.warning("No data available.")

# CSS
st.markdown("""
    <style>
        .download-button-container {
            display: flex;
            justify-content: center;
            margin-top: 50px;
        }
        .download-button {
            background-color: #FFD09B;  
            color: black;
            border: none;
            padding: 15px 25px;
            font-size: 16px;
            border-radius: 5px;
            cursor: pointer;
        }
        .download-button:hover {
            background-color: #FFB0B0;  
        }
    </style>
    """, unsafe_allow_html=True)

# Button to download data as CSV file with custom styles
csv = df.to_csv(index=False)
st.markdown('<div class="download-button-container"><button class="download-button" onclick="window.location.href=\'data:text/csv;charset=utf-8,' + csv + '\'">Download Data as CSV</button></div>', unsafe_allow_html=True)
