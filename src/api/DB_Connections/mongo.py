"""Takes care of the communication with the MongoDB database."""

import ast
from typing import Any

from pymongo import MongoClient

from src.api import json_converter as jsc
from src.api.login_objects import MongoLogin


class DataBase:
    """
    Represents an object which communicates with a MongoDB database.

    attributes:
        client:     MongoClient instance
        conn:       Connection instance to communicate with a MongoDB database
        collection: Selection of a specific collection
    """

    def __init__(self, login: MongoLogin) -> None:
        """Inits the Database object."""

        self.client = MongoClient(login.host)
        self.conn = self.client[login.db]
        self.collection = login.collection

    def get_data(self, atts: list, limit: int) -> list[dict]:
        """
        Extracts data from the database based on arguments which specifies the query.

        :param atts:        Attributes as search terms
        :param limit:       Number of entries in the resulting dataframe
        :return:            List of dictionaries as result of the query and the result as a JSON-file
        """

        projection = {}
        if atts:
            projection = {att: 1 for att in atts}

        data = self.get_data_from_query(query=projection, limit=limit)

        return data

    def get_data_from_query(self, query: str | dict, filter_dict: dict = None, **kwargs: Any) -> list[dict]:
        """
        Extracts data from the database based on a query.

        :param query:   Query for extracting data from the database, this can be
            a string or a dict for MongoDB
        :param filter_dict:  Specifies which data should be filtered.
        :param kwargs:  Additional Arguments to specify the query,
            actually 'limit' is supported for MongoDB
        :return:        List of dictionaries as result of the query
        """

        # MongoClient only handles dicts, so we need to evaluate a string as a dict if it has the right format
        if isinstance(query, str):
            query = ast.literal_eval(query)

        if not filter_dict:
            filter_dict = {}

        # We don't need the object-id from Mongo
        query['_id'] = 0

        data = []

        try:
            coll = self.conn[self.collection]
            cursor = coll.find(filter_dict, query)

            if "limit" in kwargs:
                cursor = cursor.limit(kwargs['limit'])

            data = list(cursor)

            jsc.convert_list_to_json(data, title="mongo")

        except Exception as e:
            print(e)

        finally:
            self._close_client()

        return data

    def _close_client(self) -> None:
        """Cleans up client resources and disconnect from MongoDB."""
        self.conn = None
        self.collection = None
        self.client.close()
