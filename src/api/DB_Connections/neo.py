"""Takes care of the communication with the neo4j database."""

import pandas as pd
from neo4j import GraphDatabase

from src.api.login_objects import NeoLogin


class DataBase:
    """
    Represents an object which communicates with a neo4j database.

    attributes:
        driver: Active driver
        conn: Connection instance to communicate with a neo4j database
    """

    def __init__(self, login: NeoLogin) -> None:
        """Inits the Database object."""

        self.driver = GraphDatabase.driver(uri=login.host,
                                           auth=(login.username, login.password))
        self.conn = self.driver.session()

    def get_data(self, elements: str, atts: list, limit: int) -> pd.DataFrame:
        """
        Extracts data from the database based on arguments which specifies the Cypher query.

        :param elements:    Represents nodes, relationships or paths
        :param atts:        Attributes of the elements as result
        :param limit:       Number of entries in the resulting dataframe
        :return:            Pandas DataFrame as result
        """

        if not atts:
            raise ValueError("You need to pass attributes to return!")

        attrs_str = ", ".join(atts)
        cypher_query = f"MATCH {elements} RETURN {attrs_str} LIMIT {limit}"

        return self.get_data_from_query(query=cypher_query)

    def get_data_from_query(self, query: str, **kwargs) -> pd.DataFrame:
        """
        Extracts data from the database based on a query.

        :param query:   Cypher query for extracting data from the database
        :param kwargs:  Not supported yet
        :return:        Pandas DataFrame as result
        """

        try:
            result = self.conn.run(query)
            data = [record.data() for record in result]
            df = pd.DataFrame(data)

        except Exception as e:
            print(e)
            df = pd.DataFrame()

        finally:
            self._close_driver()

        return df

    def _close_driver(self) -> None:
        """Shuts down, closing any open connections in the pool."""
        self.conn = None
        self.driver.close()
