"""This module represents a collection of data gathered from the databases"""
from typing import Any

import pandas as pd
import psycopg2
from neo4j import GraphDatabase
from pymongo import MongoClient

from src.api import constants as c
import credentials as creds


class DataCart:

    def __init__(self) -> None:
        self.data: pd.DataFrame = pd.DataFrame()
        self.bulk_data: dict[str, pd.DataFrame] = {}

    def fetch_all_data(self) -> dict:
        self.bulk_data["postgres"] = self.fetch_data_from_postgres()
        self.bulk_data["mongo"] = self.fetch_data_from_mongo()
        self.bulk_data["neo4j"] = self.fetch_data_from_neo()

    def load(self, is_bulk: bool = False) -> Any:
        """
        Returns all data stored while the instance exists

        :param is_bulk: Decides whether merged data should be returned or bulk data
        """
        if is_bulk:
            return self.bulk_data

        return self.data

    @staticmethod
    def fetch_data_from_postgres():
        conn = None
        try:
            conn = psycopg2.connect(
                dbname="postgres",
                user="postgres",
                password=creds.POSTGRES_PASSWORD,
                host="localhost",
                port="5432"
            )
            dataframe = pd.read_sql(c.POSTGRES_QUERY, conn)

            return dataframe

        except Exception as e:
            print("Error while fetching data from PostgreSQL", e)

        finally:
            if conn:
                conn.close()

    @staticmethod
    def fetch_data_from_mongo():
        client = None
        try:
            client = MongoClient("mongodb://localhost:27017/")
            db = client["mongo"]
            collection = db["ausgaben"]

            data = list(collection.find(c.MONGO_QUERY))
            dataframe = pd.DataFrame(data)

            return dataframe

        except Exception as e:
            print("Error while fetching data from MongoDB", e)

        finally:
            if client:
                client.close()

    @staticmethod
    def fetch_data_from_neo():
        driver = None
        session = None
        uri = "bolt://localhost:7687"

        try:
            driver = GraphDatabase.driver(uri, auth=("neo4j", creds.NEO4J_PASSWORD))
            session = driver.session()

            result = session.run(c.NEO4J_QUERY)
            data = [record["n"] for record in result]
            dataframe = pd.DataFrame([dict(record) for record in data])

            return dataframe

        except Exception as e:
            print("Error while fetching data from neo4j", e)

        finally:
            if driver:
                driver.close()
            if session:
                session.close()


