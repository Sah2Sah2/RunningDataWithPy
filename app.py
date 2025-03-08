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

    # Remove "Unknown" 
    if df is not None:
        # Apply filter based on shoe
        selected_shoe = st.sidebar.selectbox("Select Shoes", ["All"] + list(df['shoes'].unique()), index=0)
        if selected_shoe != "All":
            df = df[df['shoes'] == selected_shoe]
            st.write(f"✅ Filter applied: {selected_shoe}")
        else:
            st.write("✅ Showing all shoes")
        
        # Remove "Unknown" 
        df = df[df['shoes'] != 'Unknown']

        # Plot
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

import streamlit as st
import pandas as pd
import base64

# CSV
csv = df.to_csv(index=False)
b64 = base64.b64encode(csv.encode()).decode()  
href = f'data:text/csv;base64,{b64}'

# Download Button & CSS
st.markdown(f"""
    <style>
        .download-button-container {{
            display: flex;
            justify-content: center;
            margin-top: 50px;
        }}
        .download-button {{
            background-color: #FFD09B;
            color: black;
            border: none;
            padding: 15px 25px;
            font-size: 16px;
            border-radius: 5px;
            cursor: pointer;
            text-decoration: none;
            display: inline-block;
        }}
        .download-button:hover {{
            background-color: #FFB0B0;
        }}
    </style>
    <div class="download-button-container">
        <a href="{href}" download="running_data.csv" class="download-button">Download Data as CSV</a>
    </div>
""", unsafe_allow_html=True)
