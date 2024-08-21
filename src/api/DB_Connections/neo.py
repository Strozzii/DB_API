import pandas as pd
from neo4j import GraphDatabase

import credentials as creds


class DataBase:

    def __init__(self) -> None:
        uri = "bolt://localhost:7687"
        username = 'neo4j'
        password = creds.NEO4J_PASSWORD

        driver = GraphDatabase.driver(uri, auth=(username, password))
        self.conn = driver.session()

    def get_data(self, query: str, atts: list, limit: int) -> pd.DataFrame:

        if not atts:
            raise ValueError

        attrs_str = ", ".join(atts)
        cypher_query = f"MATCH {query} RETURN {attrs_str} LIMIT {limit}"

        try:

            result = self.conn.run(cypher_query)

            data = [record.data() for record in result]

            df = pd.DataFrame(data)
        except Exception as e:
            print(e)
            df = pd.DataFrame()

        return df

    def get_data_from_query(self, query: str) -> pd.DataFrame:

        try:
            result = self.conn.run(query)
            data = [record.data() for record in result]
            df = pd.DataFrame(data)
        except Exception as e:
            print(e)
            df = pd.DataFrame()

        return df
