"""This module takes care of the exchange between frontend and backend."""

from typing import Any, Union

import pandas as pd

from src.api.login_objects import MongoLogin, NeoLogin
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

    Attributes:
        db: Instance for communication with supported database technologies (PostgreSQL, MongoDB, neo4j)
    """

    def __init__(self) -> None:
        """Inits the DataManager Class."""

        self.db = None

    def get_data(self, query: str | dict, **kwargs: Any) -> Union[pd.DataFrame, list[dict]]:
        """
        Calls any database-object based on the syntax of the query.

        :param query:   Query for extracting data from the database, this can be
                        a string for everything or a dict for MongoDB
        :param kwargs:  Additional Arguments to specify the query
        :return:        Based on the database type, the result is a Pandas DataFrame or a list of dictionaries,
                        but a JSON file is always exported
        """

        # The analyzer does not need to worry about the query being available
        if not query:
            raise ValueError("You need to pass a query to get a response!")

        syntax = analyze_query(query=query)

        match syntax:
            case Syntax.POSTGRES:
                self.db = Postgres()
            case Syntax.MONGO:
                self.db = Mongo()
            case Syntax.NEO:
                self.db = Neo()
            case _:
                raise ValueError("Your query is not valid or not supported yet...")

        return self.db.get_data_from_query(query=query, **kwargs)

    def get_postgres_data(self, table: str, atts: list, limit: int = 365) -> pd.DataFrame:
        """
        Calls the Postgres-object to communicate with a PostgreSQL database.

        :param table:   Specifies the table (e.g. FROM <table>)
        :param atts:    Specifies the attributes (e.g. SELECT <atts>)
        :param limit:   Specifies the number of entries in the result (default: 365)
        :return:        Pandas DataFrame as result and the result as JSON-file
        """

        self.db = Postgres()
        return self.db.get_data(table=table,
                                atts=atts,
                                limit=limit)

    def get_mongo_data(self, atts: list, limit: int = 100) -> list[dict]:
        """
        Calls the Mongo-object to communicate with a MongoDB database.

        :param atts:        Attributes as search terms
        :param limit:       Number of entries in the resulting dataframe (default: 100)
        :return:            List of dictionaries as result and the result as JSON-file
        """

        self.db = Mongo()
        return self.db.get_data(atts=atts,
                                limit=limit)

    def get_neo_data(self, elements: str, atts: list, limit: int = 100) -> list[dict]:
        """
        Calls the Neo-object to communicate with a neo4j database.

        :param elements:    Represents nodes, relationships or paths
        :param atts:        Attributes of the elements as result
        :param limit:       Number of entries in the resulting dataframe (default: 100)
        :return:            List of dictionaries as result and the result as JSON-file
        """
        self.db = Neo()
        return self.db.get_data(elements=elements,
                                atts=atts,
                                limit=limit)

    def get_expenses_by_date(self, start: str = "", end: str = "") -> pd.DataFrame:
        """
        Explicit method call to get entries in a specific date range.

        :param start:   Start interval
        :param end:     End interval
        :return:        Pandas DataFrame as result and the result as JSON-file
        """

        self.db = FinanceDB()

        return self.db.get_expenses_by_date(start=start, end=end)

    def get_mitigation_plan(self, risk_id: str) -> list[dict]:
        """
        Explicit method call to get entries for a specific risk.

        :param risk_id: ID of the specific risk
        :return:        List of dictionaries as result and the result as JSON-file
        """

        self.db = RiskDB()

        return self.db.get_mitigation_plan(risk_id=risk_id)

    def get_all_project_leader(self):
        """
        Explicit method call to get entries with all employees as project leaders.

        :return: List of dictionaries as result and the result as JSON-file
        """

        self.db = TeamsDB()

        return self.db.get_all_project_leader()
