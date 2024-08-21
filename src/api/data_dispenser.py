"""This module takes care of the exchange between frontend and backend."""

from typing import Any

import pandas as pd

from src.api.query_analyzer import Syntax, analyze_query
from src.api.DB_Connections.postgres import DataBase as Postgres
from src.api.DB_Connections.neo import DataBase as Neo
from src.api.DB_Connections.mongo import DataBase as Mongo


class DataDispenser:
    """
    Represents the API object.
    All databases need to be implemented as instance variables.

    Attributes:
        postgres:   Instance of a Postgres-Object to use methods on a PostgreSQL database
        neo:        Instance of a Neo-Object to use methods on a neo4j database
        mongo:      Instance of a Mongo-Object to use methods on a mongo database
    """

    def __init__(self) -> None:
        """Inits the DataCart Class."""

        self.postgres = Postgres()
        self.neo = Neo()
        self.mongo = Mongo()

    def get_data(self, query: str | dict, **kwargs: Any) -> pd.DataFrame:
        """
        Calls any database-object based on the syntax of the query.

        :param query: Query for extracting data from the database, this can be
            a string for everything or a dict for MongoDB
        :param kwargs: Additional Arguments to specify the query,
            actually 'collection' and 'limit' are supported for MongoDB
        :return: Pandas DataFrame as result
        """

        # The analyser does not need to worry about the query being available
        if not query:
            raise ValueError("You need to pass a query to get a response!")

        syntax = analyze_query(query=query)

        match syntax:
            case Syntax.POSTGRES:
                return self.postgres.get_data_from_query(query=query)
            case Syntax.MONGO:
                return self.mongo.get_data_from_query(query=query, **kwargs)
            case Syntax.NEO:
                return self.neo.get_data_from_query(query=query)
            case _:
                raise ValueError("Your query is not valid or not supported yet...")

    def get_postgres_data(self, table: str, atts: list, limit: int = 365) -> pd.DataFrame:
        """
        Calls the Postgres-object to communicate with the PostgreSQL database.

        :param table:   Specifies the table (e.g. FROM <table>)
        :param atts:    Specifies the attributes (e.g. SELECT <atts>)
        :param limit:   Specifies the number of entries in the result (default: 365)
        :return:        Pandas DataFrame as result
        """

        return self.postgres.get_data(table=table,
                                      atts=atts,
                                      limit=limit)

    def get_mongo_data(self, collection: str, atts: list, limit: int = 100) -> pd.DataFrame:
        """
        Calls the Mongo-object to communicate with the MongoDB database.

        :param collection:  Specifies the collection in the MongoDB-Server
        :param atts:        Attributes as search terms
        :param limit:       Number of entries in the resulting dataframe (default: 100)
        :return:            Pandas DataFrame as result
        """

        return self.mongo.get_data(collection=collection,
                                   atts=atts,
                                   limit=limit)

    def get_neo_data(self, elements: str, atts: list, limit: int = 100) -> pd.DataFrame:
        """
        Calls the Neo-object to communicate with the neo4j database.

        :param elements:    Represents nodes, relationships or paths
        :param atts:        Attributes of the elements as result
        :param limit:       Number of entries in the resulting dataframe (default: 100)
        :return:            Pandas DataFrame as result
        """
        return self.neo.get_data(elements=elements,
                                 atts=atts,
                                 limit=limit)







