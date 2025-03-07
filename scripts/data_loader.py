import os
import pymongo
import pandas as pd
from datetime import datetime

def load_running_data():
    # MongoDB connection
    uri = os.getenv("MongoDB_ConnectionString")  # Fetch URI from ENV VAR
    client = pymongo.MongoClient(uri)
    db = client.get_database("strava_data")
    collection = db.get_collection("activities")
    
    # Fetch activities from 2024
    pipeline = [
        {"$match": {"timestamp": {"$gte": datetime(2024, 1, 1), "$lt": datetime(2025, 1, 1)}}},  # Filter for activities in 2024
        {"$project": {  # Relevant fields
            "timestamp": 1,
            "distance": 1,  
            "elevation_gain": 1,
            "elevation_loss": 1,
            "avg_pace": 1,  
            "shoes": 1,
            "calories": 1,
        }},
    ]
    
    activities = list(collection.aggregate(pipeline))
    
    if not activities:
        return None
    
    df = pd.DataFrame(activities)
    
    # Debugging
    print(f"Columns in DataFrame: {df.columns.tolist()}")
    print(df.head(10))

    if 'distance' not in df.columns or 'avg_pace' not in df.columns:
        print("Error: 'distance' or 'avg_pace' column is missing.")
        return None  
    
    # Check for missing values in 'shoes' column
    if df['shoes'].isnull().any():
        print("Warning: Missing values in the 'shoes' column.")
        df['shoes'].fillna("Unknown", inplace=True)
    
    # Convert timestamp to datetime
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    # Check for missing values in key columns
    missing_values = df[['distance', 'avg_pace']].isnull().sum()
    if missing_values.any():
        print(f"Missing values found in the following columns:\n{missing_values}")
    
    # Ensure correct data types
    df['distance'] = pd.to_numeric(df['distance'], errors='coerce')  
    df['avg_pace'] = pd.to_numeric(df['avg_pace'], errors='coerce')  
    
    if df[['distance', 'avg_pace']].isnull().any().any():
        print("NaN values found in the columns after conversion.")
        return None 
    
    # Calculate distance in km
    df['distance_km'] = df['distance']
    
    # Calculate pace in min/km
    df['pace_min_per_km'] = df['avg_pace']

    # Calculate moving average pace
    df['moving_avg_pace'] = df['pace_min_per_km'].rolling(window=3).mean()
    
    # Include columns in DF to process the data and plotting
    df = df[['timestamp', 'distance_km', 'pace_min_per_km', 'elevation_gain', 'shoes', 'calories']]
    
    # Calculate the fastest pace for shoes
    fastest_paces = df.groupby('shoes')['pace_min_per_km'].min().reset_index()
    fastest_paces = fastest_paces.rename(columns={'pace_min_per_km': 'fastest_pace_min_per_km'})
    
    # Add the fastest paces with the original DF
    df = pd.merge(df, fastest_paces, on='shoes', how='left')
    
    # Debugging
    print(f"Fastest paces per shoe:\n{fastest_paces}")
    
    return df


