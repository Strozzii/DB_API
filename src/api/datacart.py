"""This module represents a collection of data gathered from the databases"""
import pandas as pd

from src.api.query_analyzer import Syntax, analyze_query
from src.api.DB_Connections.postgres import DataBase as Postgres
from src.api.DB_Connections.neo import DataBase as Neo
from src.api.DB_Connections.mongo import DataBase as Mongo


class DataCart:

    def __init__(self) -> None:
        self.postgres = Postgres()
        self.neo = Neo()
        self.mongo = Mongo()

    def get_data(self, query: str | dict, **kwargs) -> pd.DataFrame:
        if not query:
            raise ValueError("You need to pass a query to get a response!")

        syntax = analyze_query(query)

        match syntax:
            case Syntax.POSTGRES:
                return self.postgres.get_data_from_query(query)
            case Syntax.MONGO:
                return self.mongo.get_data_from_query(query, **kwargs)
            case Syntax.NEO:
                return self.neo.get_data_from_query(query)
            case _:
                raise ValueError("Your query is not valid or not supported yet...")

    def get_postgres_data(self, table: str, atts: list, limit: int = 365) -> pd.DataFrame:
        return self.postgres.get_data(table=table, atts=atts, limit=limit)

    def get_mongo_data(self, collection: str, atts: list, limit: int = 100):
        return self.mongo.get_data(collection=collection, atts=atts, limit=limit)

    def get_neo_data(self, query: str, atts: list, limit: int = 100):
        return self.neo.get_data(query=query, atts=atts, limit=limit)







