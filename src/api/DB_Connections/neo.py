"""Takes care of the communication with the neo4j database."""

import pandas as pd
from neo4j import GraphDatabase

import credentials as creds


class DataBase:
    """
    Represents an object which communicates with a neo4j database.

    attributes:
        conn: Connection instance to communicate with a neo4j database
    """

    def __init__(self) -> None:
        """Inits the Database object."""

        driver = GraphDatabase.driver(uri=creds.NEO["uri"],
                                      auth=(creds.NEO["username"], creds.NEO["password"]))
        self.conn = driver.session()

    def get_data(self, elements: str, atts: list, limit: int) -> pd.DataFrame:
        """
        Extracts data from the database based on arguments which specifies the Cypher query.

        :param elements:    Represents nodes, relationships or paths
        :param atts:        Attributes of the elements as result
        :param limit:       Number of entries in the resulting dataframe
        :return:            Pandas DataFrame as result
        """

        if not atts:
            raise ValueError

        attrs_str = ", ".join(atts)
        cypher_query = f"MATCH {elements} RETURN {attrs_str} LIMIT {limit}"

        try:

            result = self.conn.run(cypher_query)

            data = [record.data() for record in result]

            df = pd.DataFrame(data)
        except Exception as e:
            print(e)
            df = pd.DataFrame()

        return df

    def get_data_from_query(self, query: str) -> pd.DataFrame:
        """
        Extracts data from the database based on a query.

        :param query:   Cypher query for extracting data from the database
        """

        try:
            result = self.conn.run(query)
            data = [record.data() for record in result]
            df = pd.DataFrame(data)
        except Exception as e:
            print(e)
            df = pd.DataFrame()

        return df
