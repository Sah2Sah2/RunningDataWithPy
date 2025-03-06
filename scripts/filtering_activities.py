import pymongo
from datetime import datetime
import os

uri = os.getenv("MongoDB_ConnectionString")  # Fetch URI from ENV VAR

try:
    client = pymongo.MongoClient(uri)
    client.admin.command('ping')  
    print("MongoDB connection successful!")
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")
    exit()

db = client.get_database("strava_data")
collection = db.get_collection("activities")

# Filter for activities from 2024
activities_2024 = collection.find({
    "timestamp": {
        "$gte": datetime(2024, 1, 1),
        "$lt": datetime(2025, 1, 1)
    }
})

# Divide by month
for activity in activities_2024:
    month_str = activity["timestamp"].strftime("%b_%Y")  
    
    collection.update_one(
        {"_id": activity["_id"]},  
        {"$set": {"month": month_str}} 
    )
    print(f"Updated activity {activity['_id']} with month: {month_str}")

    # Access or create a collection for the specific month
    month_collection = db.get_collection(f"activities_{month_str}")
    
    # Insert the activity into the respective month collection
    month_collection.insert_one(activity)
    print(f"Inserted activity into {month_str} collection: {activity['timestamp']}")

print("Activities successfully divided by month and tagged!")
