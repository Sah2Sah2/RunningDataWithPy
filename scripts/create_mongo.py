import os
import pymongo
import pandas as pd
from datetime import datetime

uri = os.getenv("MongoDB_ConnectionString")  # Fetch URI from ENV VAR

# Check if connection is working by listing databases
try:
    client = pymongo.MongoClient(uri)
    client.admin.command('ping')  
    print("MongoDB connection successful!")
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")
    exit()

# Access the MongoDB database and collection
db = client.get_database("strava_data")
collection = db.get_collection("activities")

# Path to the CSV file
csv_file = r"temp_folder\activities.csv"  

# Read CSV file using pandas
try:
    df = pd.read_csv(csv_file)
    print(f"CSV file loaded successfully. {len(df)} rows found.")
except Exception as e:
    print(f"Error reading CSV file: {e}")
    exit()

# Process the CSV file to filter running activities
for index, row in df.iterrows():
    # Filter for running activities
    try:
        if row['Activity Type'] == 'Run':
            timestamp = pd.to_datetime(row['Activity Date'])
            
            avg_pace = round(60 / (row['Average Speed'] * 3.6), 2) if row['Average Speed'] != 0 else None  
            
            # Create the activity document
            activity = {
                "activity_type": row['Activity Type'],
                "timestamp": timestamp,
                "distance": round(row['Distance'], 2),  
                "elevation_gain": row['Elevation Gain'],
                "elevation_loss": row['Elevation Loss'],
                "elevation_low": row['Elevation Low'],
                "elevation_high": row['Elevation High'],
                "avg_pace": avg_pace,
                "shoes": row['Activity Gear'], 
                "filename": row['Filename'],
                "max_speed": row['Max Speed'],
                "max_heart_rate": row['Max Heart Rate'],
                "average_heart_rate": row['Average Heart Rate'],
                "total_work": row['Total Work'],
                "calories": row['Calories']
            }

            # Insert the activity into MongoDB
            collection.insert_one(activity)
            print(f"Uploaded: {activity['timestamp']} - {activity['distance']} km")
    except Exception as e:
        print(f"Error processing row {index}: {e}")

# Check if the data was inserted successfully 
print("Documents in activities collection after insert:")
for doc in collection.find():
    print(doc)

print("Running activities uploaded successfully!")
