"""Takes care of the communication with the MongoDB database."""

import ast
from typing import Any

import pandas as pd
from pymongo import MongoClient

import credentials as creds


class DataBase:
    """
    Represents an object which communicates with a MongoDB database.

    attributes:
        conn: Connection instance to communicate with a MongoDB database
    """

    def __init__(self):
        """Inits the Database object."""

        client = MongoClient(creds.MONGO["host"])
        self.conn = client[creds.MONGO["db"]]

    def get_data(self, collection: str, atts: list, limit: int) -> pd.DataFrame:
        """
        Extracts data from the database based on arguments which specifies the query.

        :param collection:  Specifies the collection in the MongoDB-Server
        :param atts:        Attributes as search terms
        :param limit:       Number of entries in the resulting dataframe
        :return:            Pandas DataFrame as result
        """

        projection = {}
        if atts:
            projection = {att: 1 for att in atts}

        # Getting rid of the objectIDs generated by mongo
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

    def get_data_from_query(self, query: str | dict, **kwargs: Any) -> pd.DataFrame:
        """
        Extracts data from the database based on a query.

        :param query:   Query for extracting data from the database, this can be
            a string for everything or a dict for MongoDB
        :param kwargs:  Additional Arguments to specify the query,
            actually 'collection' and 'limit' are supported for MongoDB
        :return:        Pandas DataFrame as result
        """

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
