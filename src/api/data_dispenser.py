"""This module takes care of the exchange between frontend and backend."""

from typing import Any

import pandas as pd

from src.api.login_objects import BaseLogin
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

        self.db = None

    def get_data(self, login: Any, query: str | dict, **kwargs: Any) -> pd.DataFrame:
        """
        Calls any database-object based on the syntax of the query.

        :param login: Login-Object to dynamically connect to a database
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
                self.db = Postgres(login=login)
            case Syntax.MONGO:
                self.db = Mongo(login=login)
            case Syntax.NEO:
                self.db = Neo(login=login)
            case _:
                raise ValueError("Your query is not valid or not supported yet...")

        return self.db.get_data_from_query(query=query, **kwargs)

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

    def get_top_x_expenses(self, x: int = 5) -> pd.DataFrame:
        """
        Explicit method call to get the top x entries by value as a result.

        :param x: Determines the number of largest entries
        :return: Result as Pandas DataFrame
        """
        return self.postgres.get_data_from_query(f"SELECT * FROM ausgaben ORDER BY amount DESC LIMIT {x}")

    def get_expenses_by_date(self, start: str = "", end: str = "") -> pd.DataFrame:
        """
        Explicit method call to get entries in a specific date range.

        :param start: Start interval
        :param end: End interval
        :return: Result as Pandas DataFrame
        """

        base_query = "SELECT * FROM ausgaben WHERE expense_date "

        if start and not end:
            base_query += f">= '{start}'"

        elif not start and end:
            base_query += f"<= '{end}'"

        elif start and end:
            base_query += f"BETWEEN '{start}' AND '{end}'"

        else:
            raise ValueError("You need to provide at least one date as start or end!")

        return self.postgres.get_data_from_query(query=base_query)









