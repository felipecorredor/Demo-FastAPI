from pymongo import MongoClient
import os

MONGO_URI = os.getenv("MONGO_URI")

db = MongoClient(MONGO_URI)

# This line selects/creates the database called "test" within the MongoDB client.
# The [] operator is used to access a specific database on the server.
# If the database does not exist,
# MongoDB will create it when you first insert data.
db_client = db["wizeline"]
