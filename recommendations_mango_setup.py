from pymongo import MongoClient
import pandas as pd
import ast  # To parse string representations of Python objects

# MongoDB connection details
MONGO_URI = "mongodb://localhost:27017/"  # Replace with your MongoDB URI
DATABASE_NAME = "recipes_db"
COLLECTION_NAME = "recipes"
MONGO_URI = "mongodb://localhost:27017/"
DATABASE_NAME = "recipes_db"
COLLECTION_NAME = "recipes"
USER_INTERACTIONS_COLLECTION = "user_interactions"
USE_DATABASE = "user"

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
collection = db[COLLECTION_NAME]

# Drop the collection if it exists to clean up
if COLLECTION_NAME in db.list_collection_names():
    collection.drop()
    print(f"Collection '{COLLECTION_NAME}' dropped and will be recreated.")
else:
    print(f"Collection '{COLLECTION_NAME}' does not exist and will be created.")

# Load recipes from the CSV file
csv_path = "./data/recipes.csv"  # Replace with the correct path to your CSV file
df = pd.read_csv(csv_path)

# Parse columns that are JSON-like strings into proper Python types
def parse_column(column):
    return column.apply(lambda x: ast.literal_eval(x) if pd.notna(x) else None)

df["ingredients"] = parse_column(df["ingredients"])
df["steps"] = parse_column(df["steps"])
df["macros"] = parse_column(df["macros"])
df["goal"] = parse_column(df["goal"])

# Convert the DataFrame to a list of dictionaries
recipes_list = df.to_dict(orient="records")

# Insert recipes into the collection
collection.insert_many(recipes_list)
print(f"Inserted {len(recipes_list)} recipes into MongoDB.")

# Close the connection
client.close()



def ensure_user_interactions_collection():
    """
    Ensures that the 'user_interactions' collection exists in the MongoDB database.
    """
    client = MongoClient(MONGO_URI)
    db = client[USE_DATABASE]

    # Check if the collection exists
    if USER_INTERACTIONS_COLLECTION not in db.list_collection_names():
        # Create the collection
        db.create_collection(USER_INTERACTIONS_COLLECTION)
        print(f"Collection '{USER_INTERACTIONS_COLLECTION}' created successfully.")
    else:
        print(f"Collection '{USER_INTERACTIONS_COLLECTION}' already exists.")

    client.close()