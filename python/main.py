import requests as req
import os, pymongo

DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_NAME = os.getenv("DB_NAME")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
print(f"mongodb://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}?authSource=admin")

BASE_URL = "https://data.regionreunion.com/api/explore/v2.1/catalog/datasets/"
COLLECTIONS = [
    "tourisme",
    "lieu"
]
DATASETS = [
    "etablissements-touristiques-lareunion-wssoubik",
    "lieux-remarquables-lareunion-wssoubik"
]

client = pymongo.MongoClient(
    f"mongodb://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}?authSource=admin",
    serverSelectionTimeoutMS=5000  # Set the timeout to 5000 milliseconds (5 seconds)
)
db = client[DB_NAME]

print("Connected to MongoDB")

for DATASET in DATASETS:

    print(f"Fetching data from {DATASET}")
    
    collection = db[COLLECTIONS[DATASETS.index(DATASET)]]
    count = int(req.get(BASE_URL + DATASET + "/records?limit=0").json()["total_count"])
    
    for i in range(0, count, 100):
        print(f"Fetching data from {DATASET} - {i}/{count}")

        resp = req.get(BASE_URL + DATASET + "/records?limit=100&offset=" + str(i))

        for result in resp.json()["results"]:
            collection.insert_one(result)