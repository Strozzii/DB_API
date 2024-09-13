"""Takes care of the communication with the neo4j database."""

import neo4j
from neo4j import GraphDatabase

from src.api import json_converter as jsc
from src.api.login_objects import NeoLogin
from src.api.datetime_handler import convert_timestamp


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

    def get_data(self, elements: str, atts: list, limit: int) -> list[dict]:
        """
        Extracts data from the database based on arguments which specifies the Cypher query.

        :param elements:    Represents nodes, relationships or paths
        :param atts:        Attributes of the elements as result
        :param limit:       Number of entries in the resulting dataframe
        :return:            List of dictionaries as result of the query and the result as a JSON-file
        """

        if not atts:
            raise ValueError("You need to pass attributes to return!")

        attrs_str = ", ".join(atts)
        cypher_query = f"MATCH {elements} RETURN {attrs_str} LIMIT {limit}"

        return self.get_data_from_query(query=cypher_query)

    def get_data_from_query(self, query: str) -> list[dict]:
        """
        Extracts data from the database based on a query.

        :param query:   Cypher query for extracting data from the database
        :return:        List of dictionaries as result of the query
        """

        records = []

        try:
            # The result is a neo4j object which needs a little bit of transformation
            result = self.conn.run(query)

            for record in result:
                record_dict = {}

                # FYI: We need to convert timestamps, cause JSON can't natively handle datetime-objects
                for key, value in record.items():

                    # The usual case for nodes
                    if isinstance(value, dict):
                        record_dict[key] = {k: convert_timestamp(v) for k, v in value.items()}

                    # The case for relationships, the format is kinda scuffed :(
                    elif isinstance(value, neo4j.graph.Relationship):
                        record_dict[key] = {
                            "type": value.type,
                            **{k: convert_timestamp(v) for k, v in dict(value).items()}
                        }
                    elif isinstance(value, str):
                        record_dict[key] = value

                    else:
                        record_dict[key] = {k: convert_timestamp(v) for k, v in dict(value).items()}

                records.append(record_dict)

            jsc.convert_list_to_json(records, "neo")

        except Exception as e:
            print(e)

        finally:
            self._close_driver()

        return records

    def _close_driver(self) -> None:
        """Shuts down, closing any open connections in the pool."""
        self.conn = None
        self.driver.close()
