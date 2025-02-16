import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from scripts.data_loader import load_running_data
from scripts.visualization import plot_monthly_trends

st.title("🏃 Running Data Dashboard")

df = load_running_data("./data/sample_running_data.csv")

if df is not None:
    st.subheader("📊 Monthly Trends")
    st.pyplot(plot_monthly_trends(df))
else:
    st.warning("No data available. Please upload a CSV file.")
