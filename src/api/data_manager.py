"""This module takes care of the exchange between frontend and backend."""

from typing import Any

import pandas as pd

from src.api.login_objects import PostgresLogin, MongoLogin, NeoLogin
from src.api.query_analyzer import Syntax, analyze_query
from src.api.DB_Connections.postgres import DataBase as Postgres
from src.api.DB_Connections.neo import DataBase as Neo
from src.api.DB_Connections.mongo import DataBase as Mongo
from src.api.DB_Scripts.risk_db import RiskDB
from src.api.DB_Scripts.finance_db import FinanceDB
from src.api.DB_Scripts.team_mapping_db import TeamsDB


class DataManager:
    """
    Represents the API object.
    All databases need to be implemented as instance variables.

    Attributes:
        db: Instance for communication with supported database technologies (PostgreSQL, MongoDB, neo4j)
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

        # The analyzer does not need to worry about the query being available
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

    def get_postgres_data(self, login: PostgresLogin, table: str, atts: list, limit: int = 365) -> pd.DataFrame:
        """
        Calls the Postgres-object to communicate with the PostgreSQL database.

        :param login:   Login-Object to dynamically connect to a Postgres database
        :param table:   Specifies the table (e.g. FROM <table>)
        :param atts:    Specifies the attributes (e.g. SELECT <atts>)
        :param limit:   Specifies the number of entries in the result (default: 365)
        :return:        Pandas DataFrame as result
        """

        self.db = Postgres(login=login)
        return self.db.get_data(table=table,
                                atts=atts,
                                limit=limit)

    def get_mongo_data(self, login: MongoLogin, atts: list, limit: int = 100) -> pd.DataFrame:
        """
        Calls the Mongo-object to communicate with the MongoDB database.

        :param login:       Login-Object to dynamically connect to a Mongo database
        :param atts:        Attributes as search terms
        :param limit:       Number of entries in the resulting dataframe (default: 100)
        :return:            Pandas DataFrame as result
        """

        self.db = Mongo(login=login)
        return self.db.get_data(atts=atts,
                                limit=limit)

    def get_neo_data(self, login: NeoLogin, elements: str, atts: list, limit: int = 100) -> pd.DataFrame:
        """
        Calls the Neo-object to communicate with the neo4j database.

        :param login:       Login-Object to dynamically connect to a Neo database
        :param elements:    Represents nodes, relationships or paths
        :param atts:        Attributes of the elements as result
        :param limit:       Number of entries in the resulting dataframe (default: 100)
        :return:            Pandas DataFrame as result
        """
        self.db = Neo(login=login)
        return self.db.get_data(elements=elements,
                                atts=atts,
                                limit=limit)

    def get_expenses_by_date(self, start: str = "", end: str = ""):
        """
        Explicit method call to get entries in a specific date range.

        :param start: Start interval
        :param end: End interval
        :return: Result as Pandas DataFrame
        """

        self.db = FinanceDB()

        return self.db.get_expenses_by_date(start=start, end=end)

    def get_mitigation_plan(self, risk_id: str):

        self.db = RiskDB()

        return self.db.get_mitigation_plan(risk_id=risk_id)

    def get_all_project_leader(self):

        self.db = TeamsDB()

        return self.db.get_all_project_leader()
