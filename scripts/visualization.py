import matplotlib.pyplot as plt
import seaborn as sns

def plot_monthly_trends(df):
    """Plot monthly running distance and pace trends."""
    df['month'] = df['date'].dt.to_period('M')
    monthly_stats = df.groupby('month').agg({'distance_km': 'sum', 'pace_min_per_km': 'mean'}).reset_index()
    
    fig, ax1 = plt.subplots(figsize=(10, 5))

    ax1.set_xlabel("Month")
    ax1.set_ylabel("Total Distance (km)", color="tab:blue")
    ax1.plot(monthly_stats["month"].astype(str), monthly_stats["distance_km"], marker='o', color="tab:blue", label="Distance")

    ax2 = ax1.twinx()
    ax2.set_ylabel("Avg Pace (min/km)", color="tab:red")
    ax2.plot(monthly_stats["month"].astype(str), monthly_stats["pace_min_per_km"], marker='s', color="tab:red", linestyle="dashed", label="Pace")

    fig.autofmt_xdate()
    plt.title("Monthly Running Trends")
    plt.show()

# Example usage
if __name__ == "__main__":
    from data_loader import load_running_data
    df = load_running_data("../data/sample_running_data.csv")
    if df is not None:
        plot_monthly_trends(df)
