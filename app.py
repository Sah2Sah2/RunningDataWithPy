import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from scripts.data_loader import load_running_data
from scripts.visualization import plot_monthly_trends

st.title("🏃🏻‍♀️ Running Data Dashboard")

# Load data from MongoDB
try:
    df = load_running_data()  
    if df is not None:
        st.subheader("📊 Monthly Trends")
        st.pyplot(plot_monthly_trends(df))  
    else:
        st.warning("No running data found for 2024.")
except Exception as e:
    st.error(f"An error occurred: {e}")