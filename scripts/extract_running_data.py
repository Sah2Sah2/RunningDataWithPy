import os
import zipfile
import pymongo
from fitparse import FitFile
from datetime import datetime

# Mongo
uri = os.getenv("MongoDB_ConnectionString")  # Fetch URI from ENV VAR
client = pymongo.MongoClient(uri)
db = client["strava_data"]
collection = db["activities"]

# Path to Strava ZIP folder
zip_folder = r"C:\Users\sarab\Downloads\export_65679332.zip\activities"
extract_folder = "temp_folder"

# Unzip Files
if not os.path.isdir(extract_folder):
    with zipfile.ZipFile(zip_folder, "r") as zip_ref:
        zip_ref.extractall(extract_folder)
    print("Files extracted successfully!")

# Function to Parse FIT Files
def parse_fit_file(fit_file):
    fitfile = FitFile(fit_file)
    activity = {"splits": []}

    for record in fitfile.get_messages("session"):
        for data in record:
            if data.name == "sport":
                activity["activity_type"] = data.value
            if data.name == "start_time":
                activity["timestamp"] = data.value
            if data.name == "total_distance":
                activity["distance"] = round(data.value / 1000, 2)  
            if data.name == "total_ascent":
                activity["elevation"] = data.value  
            if data.name == "avg_speed":
                avg_speed = data.value * 3.6 
                activity["avg_pace"] = round(60 / avg_speed, 2) if avg_speed != 0 else None
            if data.name == "sport" and data.value == "running":
                activity["shoes"] = "Nike Pegasus"  

    # Get Splits 
    for lap in fitfile.get_messages("lap"):
        split = {}
        for data in lap:
            if data.name == "total_distance":
                split["distance"] = round(data.value / 1000, 2)
            if data.name == "total_elapsed_time":
                split["time"] = int(data.value) 
        if split:
            activity["splits"].append(split)

    # Filter by running activities in 2024
    if activity.get("activity_type") == "running" and activity.get("timestamp"):
        if activity["timestamp"].year == 2024:
            return activity
    
    return None

# Process .fit Files
for root, _, files in os.walk(extract_folder):
    for file in files:
        if file.endswith(".fit"):
            file_path = os.path.join(root, file)
            with open(file_path, "rb") as fit_file:
                data = parse_fit_file(fit_file)
                if data:
                    collection.insert_one(data)
                    print(f"Uploaded: {data['timestamp']}")

print("Running activities uploaded successfully!")
