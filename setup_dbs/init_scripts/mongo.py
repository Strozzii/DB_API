import json
import os.path
from pymongo import MongoClient


def setup():
    client = MongoClient('mongodb://localhost:27017/')
    db = client['mongo']
    collection = db['risks']

    collection.drop()

    json_file_path = os.path.join(os.path.dirname(__file__), 'configuration/risk_data.json')

    with open(json_file_path, 'r') as file:
        data = json.load(file)

    for record in data:
        collection.insert_one(record)
