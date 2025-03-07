import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd  

def plot_monthly_trends(df):
    """Plot monthly running distance and pace trends."""
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['month'] = df['timestamp'].dt.to_period('M')
    
    monthly_stats = df.groupby('month').agg({
        'distance_km': 'sum',
        'pace_min_per_km': 'mean'
    }).reset_index()
    
    fig, ax1 = plt.subplots(figsize=(10, 5))
    ax1.set_xlabel("Month")
    ax1.set_ylabel("Total Distance (km)", color="tab:blue")
    ax1.plot(monthly_stats["month"].astype(str), monthly_stats["distance_km"], marker='o', color="tab:blue", label="Distance")

    ax2 = ax1.twinx()
    ax2.set_ylabel("Avg Pace (min/km)", color="tab:red")
    ax2.plot(monthly_stats["month"].astype(str), monthly_stats["pace_min_per_km"], marker='s', color="tab:red", linestyle="dashed", label="Pace")

    fig.autofmt_xdate()
    plt.title("Monthly Running Trends")
    return fig

def plot_shoes_usage(df):
    """Pie chart for shoe usage in 2024."""
    shoe_counts = df['shoes'].value_counts()
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie(shoe_counts, labels=shoe_counts.index, autopct='%1.1f%%', startangle=90, colors=sns.color_palette("pastel"))
    ax.set_title("Shoes Usage in 2024")
    return fig

def plot_elevation_gain(df):
    """Plot monthly elevation gain."""
    df['month'] = df['timestamp'].dt.to_period('M')
    df['elevation_gain'] = df['elevation_gain'].fillna(0)
    df['elevation_gain'] = pd.to_numeric(df['elevation_gain'], errors='coerce')

    monthly_elevation = df.groupby('month')['elevation_gain'].sum().reset_index()

    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(x=monthly_elevation['month'].astype(str), y=monthly_elevation['elevation_gain'], color="green", ax=ax)
    ax.set_xlabel("Month")
    ax.set_ylabel("Total Elevation Gain (m)")
    ax.set_title("Monthly Elevation Gain")
    fig.autofmt_xdate()
    return fig

def plot_monthly_distance(df):
    """Bar plot for total monthly distance."""
    df['month'] = df['timestamp'].dt.to_period('M')
    monthly_distance = df.groupby('month')['distance_km'].sum().reset_index()

    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(x=monthly_distance['month'].astype(str), y=monthly_distance['distance_km'], color="blue", ax=ax)
    ax.set_xlabel("Month")
    ax.set_ylabel("Total Distance (km)")
    ax.set_title("Monthly Distance")
    fig.autofmt_xdate()
    return fig

if __name__ == "__main__":
    from data_loader import load_running_data
    df = load_running_data()
    
    if df is not None:
        print("Displaying Plots")
        plt.figure()
        plot_monthly_trends(df)
        plt.figure()
        plot_shoes_usage(df)
        plt.figure()
        plot_elevation_gain(df)
        plt.figure()
        plot_monthly_distance(df)
        plt.show()

        
