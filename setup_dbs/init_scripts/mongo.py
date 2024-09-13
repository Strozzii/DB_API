"""This module sets up a mongo server."""

import json
import os.path

from pymongo import MongoClient

from credentials import MongoLogin as ml


def setup():
    """Clears the existing Mongo database and populates it with test risk data from a json-file."""

    client = MongoClient(ml.host)
    db = client[ml.db]
    collection = db[ml.collection]

    collection.drop()

    json_file_path = os.path.join(os.path.dirname(__file__), 'configuration/risk_data.json')

    with open(json_file_path, 'r') as file:
        data = json.load(file)

    for record in data:
        collection.insert_one(record)
