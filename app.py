import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import base64
from fpdf import FPDF
from scripts.data_loader import load_running_data
from scripts.visualization import (
    plot_fastest_pace_per_shoe,
    plot_monthly_trends,
    plot_shoes_usage,
    plot_elevation_gain,
    plot_monthly_distance
)
from io import BytesIO
import tempfile

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
        monthly_trends_fig = plot_monthly_trends(df)
        st.pyplot(monthly_trends_fig)  

        st.subheader("👟 Shoes Usage")
        shoes_usage_fig = plot_shoes_usage(df)
        st.pyplot(shoes_usage_fig)

        st.subheader("⛰️ Monthly Elevation Gain")
        elevation_gain_fig = plot_elevation_gain(df)
        st.pyplot(elevation_gain_fig)

        st.subheader("📍 Monthly Distance")
        monthly_distance_fig = plot_monthly_distance(df)
        st.pyplot(monthly_distance_fig)

        st.subheader("🚀 Fastest Pace per Shoe")
        fastest_pace_fig = plot_fastest_pace_per_shoe(df)  
        st.pyplot(fastest_pace_fig)

    else:
        st.warning("No running data found for 2024.")

except Exception as e:
    st.error(f"An error occurred: {e}")

# Generate CSV for download
csv = df.to_csv(index=False)
b64_csv = base64.b64encode(csv.encode()).decode()  
href_csv = f'data:text/csv;base64,{b64_csv}'

# Generate PDF for download
pdf = FPDF()

def save_plot_to_bytes(fig):
    """Save a Matplotlib figure to a BytesIO object"""
    img_stream = BytesIO()
    fig.savefig(img_stream, format='png')
    img_stream.seek(0)
    return img_stream

monthly_trends_img = save_plot_to_bytes(monthly_trends_fig)
shoes_usage_img = save_plot_to_bytes(shoes_usage_fig)
elevation_gain_img = save_plot_to_bytes(elevation_gain_fig)
monthly_distance_img = save_plot_to_bytes(monthly_distance_fig)
fastest_pace_img = save_plot_to_bytes(fastest_pace_fig)

def save_image_to_tempfile(image_stream):
    """Save image from BytesIO stream to a temporary file."""
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
    temp_file.write(image_stream.read())
    temp_file.close()
    return temp_file.name

monthly_trends_temp = save_image_to_tempfile(monthly_trends_img)
shoes_usage_temp = save_image_to_tempfile(shoes_usage_img)
elevation_gain_temp = save_image_to_tempfile(elevation_gain_img)
monthly_distance_temp = save_image_to_tempfile(monthly_distance_img)
fastest_pace_temp = save_image_to_tempfile(fastest_pace_img)

# New page
def add_image_to_new_page(pdf, image_path):
    """Add image to a new page in the PDF."""
    pdf.add_page()  # new page to fit them all 
    pdf.image(image_path, x=10, y=30, w=180)

# Add images to the PDF
add_image_to_new_page(pdf, monthly_trends_temp)
add_image_to_new_page(pdf, shoes_usage_temp)
add_image_to_new_page(pdf, elevation_gain_temp)
add_image_to_new_page(pdf, monthly_distance_temp)
add_image_to_new_page(pdf, fastest_pace_temp)

# Create PDF
pdf_output = pdf.output(dest='S').encode('latin1') 
pdf_output_io = BytesIO(pdf_output)  
pdf_output_io.seek(0)  

# Convert PDF to base64
b64_pdf = base64.b64encode(pdf_output_io.read()).decode()
href_pdf = f"data:application/pdf;base64,{b64_pdf}"

# CSS for download buttons
st.markdown(f"""
    <style>
        .download-button-container {{
            display: flex;
            justify-content: center;
            gap: 20px;
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
        <a href="{href_csv}" download="running_data.csv" class="download-button">Download Running Data as CSV</a>
        <a href="{href_pdf}" download="running_data.pdf" class="download-button">Download Charts as PDF</a>
    </div>
""", unsafe_allow_html=True)


