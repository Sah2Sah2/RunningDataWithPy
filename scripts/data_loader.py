import pandas as pd

def load_running_data(filepath):
    """Load and clean running data from a CSV file."""
    try:
        df = pd.read_csv(filepath)
        
        # Convert date column to datetime
        df['date'] = pd.to_datetime(df['date'])
        
        # Ensure numeric columns are correctly typed
        df['distance_km'] = pd.to_numeric(df['distance_km'], errors='coerce')
        df['pace_min_per_km'] = pd.to_numeric(df['pace_min_km'], errors='coerce')
        
        return df
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

# Example usage
if __name__ == "__main__":
    df = load_running_data("../data/sample_running_data.csv")
    print(df.head())
