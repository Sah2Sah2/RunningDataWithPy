import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd  
import numpy as np 

# Line chart for monthly trends (pace and kms)
def plot_monthly_trends(df):
    """Plot monthly running distance and pace trends with pastel colors."""
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['month'] = df['timestamp'].dt.to_period('M')
    
    monthly_stats = df.groupby('month').agg({
        'distance_km': 'sum',
        'pace_min_per_km': 'mean'
    }).reset_index()
    
    fig, ax1 = plt.subplots(figsize=(10, 5))
    ax1.set_xlabel("Month")
    ax1.set_ylabel("Total Distance (km)", color="tab:blue")
    
    # Pastel Blue for distance
    pastel_blue = sns.color_palette("Blues")[2]
    ax1.plot(monthly_stats["month"].astype(str), monthly_stats["distance_km"], marker='o', color=pastel_blue, label="Distance")

    ax2 = ax1.twinx()
    ax2.set_ylabel("Avg Pace (min/km)", color="tab:red")
    
    # Pastel Red for pace
    pastel_red = sns.color_palette("Reds")[2]
    ax2.plot(monthly_stats["month"].astype(str), monthly_stats["pace_min_per_km"], marker='s', color=pastel_red, linestyle="dashed", label="Pace")

    fig.autofmt_xdate()
    plt.title("Monthly Running Trends", fontsize=18, loc='center', pad=20)
    return fig

# Pie chart for shoes usage 
def plot_shoes_usage(df):
    """Pie chart for shoe usage in 2024."""
    shoe_counts = df['shoes'].value_counts()
    fig, ax = plt.subplots(figsize=(8, 8))

    def autopct_func(pct, allvals):
        # do not display % labels for % < than 4
        return f'{pct:.1f}%' if pct >= 4 else ''

    # Create the pie chart
    wedges, texts, autotexts = ax.pie(shoe_counts, labels=shoe_counts.index, autopct=lambda pct: autopct_func(pct, shoe_counts),
                                       startangle=90, colors=sns.color_palette("pastel"), textprops={'fontsize': 10})

    # Optimize space to a better visualization experience
    # Find the two smallest slices 
    small_slices_threshold = 5  # < than 5%
    small_slices_indices = [i for i, count in enumerate(shoe_counts) if count < small_slices_threshold]

    for i, text in enumerate(texts):
        angle = (wedges[i].theta2 + wedges[i].theta1) / 2  # Calculate middle angle of the slice

        # For small slices = further apart
        if shoe_counts[i] < small_slices_threshold:
            # If it's one of the two smallest slices, give it extra space
            if i == small_slices_indices[0]:
                offset = 1.25 # Slightly reduce the offset for the first smallest slice
            elif i == small_slices_indices[1]:
                offset = 1.3  # Slightly reduce the offset for the second smallest slice
            else:
                offset = 1.1 + (i * 0.03)  # Reduce the offset for other small slices to be closer

            text.set_position((offset * np.cos(np.radians(angle)), offset * np.sin(np.radians(angle))))
        else:
            # Larger slices
            offset = 1.2  
            text.set_position((offset * np.cos(np.radians(angle)), offset * np.sin(np.radians(angle))))

        # Adjust the label's alignment based on its position
        if np.cos(np.radians(angle)) < 0:
            text.set_horizontalalignment('right')
        else:
            text.set_horizontalalignment('left')

    # Adjust percentage text positioning to fit in smaller slices
    for i, autotext in enumerate(autotexts):
        angle = (wedges[i].theta2 + wedges[i].theta1) / 2  # Calculate angle for each slice
        offset = 0.7  # Move percentage labels slightly toward the outer edge 
        autotext.set_position((offset * np.cos(np.radians(angle)), offset * np.sin(np.radians(angle))))
        autotext.set_fontsize(10)
        autotext.set_fontweight('bold')

    # Set title with more padding to avoid overlap
    ax.set_title("Shoes Usage in 2024", fontsize=18, loc='center', pad=20)

    return fig

# Bar chart for positive elevation gain
def plot_elevation_gain(df):
    """Plot monthly elevation gain with pastel green color."""
    df['month'] = df['timestamp'].dt.to_period('M')
    df['elevation_gain'] = df['elevation_gain'].fillna(0)
    df['elevation_gain'] = pd.to_numeric(df['elevation_gain'], errors='coerce')

    monthly_elevation = df.groupby('month')['elevation_gain'].sum().reset_index()

    fig, ax = plt.subplots(figsize=(10, 5))
    
    # Pastel green 
    pastel_green = sns.color_palette("Greens")[2]  
    sns.barplot(x=monthly_elevation['month'].astype(str), y=monthly_elevation['elevation_gain'], color=pastel_green, ax=ax)
    
    ax.set_xlabel("Month")
    ax.set_ylabel("Total Elevation Gain (m)")
    ax.set_title("Monthly Elevation Gain", fontsize=18, loc='center', pad=20)
    fig.autofmt_xdate()
    return fig

# Bar chart for monthly distance
def plot_monthly_distance(df):
    """Bar plot for total monthly distance with pastel blue color."""
    df['month'] = df['timestamp'].dt.to_period('M')
    monthly_distance = df.groupby('month')['distance_km'].sum().reset_index()

    fig, ax = plt.subplots(figsize=(10, 5))
    
    # Pastel blue 
    pastel_blue = sns.color_palette("Blues")[2]  
    sns.barplot(x=monthly_distance['month'].astype(str), y=monthly_distance['distance_km'], color=pastel_blue, ax=ax)
    
    ax.set_xlabel("Month")
    ax.set_ylabel("Total Distance (km)")
    ax.set_title("Monthly Distance", fontsize=18, loc='center', pad=20)
    fig.autofmt_xdate()
    return fig

# Dot plot for fastest pace for shoe
def plot_fastest_pace_per_shoe(df):
    """Dot plot for the fastest pace done with each shoe, excluding 'Unknown' shoes."""
    # Remove 'Unknown'
    df = df[df['shoes'] != 'Unknown']

    # Calculate the fastest pace for each shoe
    fastest_paces = df.groupby('shoes')['fastest_pace_min_per_km'].min().reset_index()

    fig, ax = plt.subplots(figsize=(10, 5))

    # Pastel color palette for dots
    pastel_colors = sns.color_palette("pastel")

    # Create the dot plot 
    sns.stripplot(x='shoes', y='fastest_pace_min_per_km', data=fastest_paces, palette=pastel_colors, ax=ax, size=8, jitter=True)

    # Add text to specify the pace next to dots
    for i, row in fastest_paces.iterrows():
        ax.text(i, row['fastest_pace_min_per_km'], f"{row['fastest_pace_min_per_km']:.2f}", 
                horizontalalignment='center', verticalalignment='bottom', fontsize=10)

    ax.set_xlabel("Shoes")
    ax.set_ylabel("Fastest Pace (min/km)")
    ax.set_title("Fastest Pace per Shoe", fontsize=18, loc='center', pad=20)
    plt.xticks(rotation=45, ha='right')  # Rotate names due to lenght

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

