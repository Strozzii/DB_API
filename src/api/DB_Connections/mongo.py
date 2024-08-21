import ast

import pandas as pd
from pymongo import MongoClient


class DataBase:

    def __init__(self):
        client = MongoClient('mongodb://localhost:27017/')
        self.conn = client['mongo']

    def get_data(self, collection: str, atts: list, limit: int) -> pd.DataFrame:

        projection = {}
        if atts:
            projection = {att: 1 for att in atts}
        projection['_id'] = 0

        try:

            coll = self.conn[collection]

            # Daten abfragen
            cursor = coll.find({}, projection)
            cursor = cursor.limit(limit)

            # Umwandeln der Cursor-Daten in eine Liste von Dictionaries
            data = list(cursor)

            # Erstellen eines DataFrames
            df = pd.DataFrame(data)
        except Exception as e:
            print(e)
            df = pd.DataFrame()

        return df

    def get_data_from_query(self, query, **kwargs) -> pd.DataFrame:
        if "collection" not in kwargs:
            raise ValueError("Collection must not be empty!")

        if isinstance(query, str):
            query = ast.literal_eval(query)

        try:
            coll = self.conn[kwargs['collection']]
            cursor = coll.find({}, query)

            if "limit" in kwargs:
                cursor = cursor.limit(kwargs['limit'])

            data = list(cursor)

            df = pd.DataFrame(data)

        except Exception as e:
            print(e)
            df = pd.DataFrame()

        return df
