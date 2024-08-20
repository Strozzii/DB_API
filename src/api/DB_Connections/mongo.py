import pandas as pd
from pymongo import MongoClient


class DataBase:

    def __init__(self):
        client = MongoClient('mongodb://localhost:27017/')
        self.conn = client['mongo']

    def get_data(self, collection: str, atts: list, limit: int) -> pd.DataFrame:

        if not atts:
            raise ValueError

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
