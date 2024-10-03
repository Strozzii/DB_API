"""Takes care of the communication with the neo4j database."""

import neo4j
from neo4j import GraphDatabase

from src.api import json_converter as jsc
from src.api.credentials import NEO_CREDS as LOGIN
from src.api.datetime_handler import convert_timestamp


class DataBase:
    """
    Represents an object which communicates with a neo4j database.

    attributes:
        conn:   Collection of all database credentials for Neo4j-databases
    """

    def __init__(self) -> None:
        """Inits the Database object."""

        self.cred = LOGIN

    def get_data_from_atts(self, elements: str, atts: list, limit: int) -> list[dict]:
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

        return self.get_data(query=cypher_query)

    def get_data(self, query: str) -> list[dict]:
        """
        Extracts data from the database based on a query.

        :param query:   Cypher query for extracting data from the database
        :return:        List of dictionaries as result of the query
        """

        records = []

        for login in self.conn.values():

            conn = GraphDatabase.driver(uri=login.host, auth=(login.username, login.password))
            session = conn.session()

            try:
                # The result is a neo4j object which needs a little bit of transformation
                result = session.run(query)

                for record in result:
                    record_dict = {}

                    # FYI: We need to convert timestamps, cause JSON can't natively handle datetime-objects
                    for key, value in record.items():

                        # The usual case for nodes
                        if isinstance(value, neo4j.graph.Node):
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
                conn.close()

        return records
