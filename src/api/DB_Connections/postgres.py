"""Takes care of the communication with the PostgreSQL database."""

import psycopg2
import pandas as pd

from src.api import json_converter as jsc
from src.api.login_objects import PostgresLogin


class DataBase:
    """
    Represents an object which communicates with a Postgres database.

    attributes:
        conn: Connection instance to communicate with a Postgres database
    """

    def __init__(self, login: PostgresLogin) -> None:
        """Inits the Database object."""

        self.conn = psycopg2.connect(
            dbname=login.dbname,
            user=login.user,
            password=login.password,
            host=login.host,
            port=login.port
        )

    def get_data(self, table: str, atts: list, limit: int) -> pd.DataFrame:
        """
        Extracts data from the database based on arguments which specifies the query.

        :param table:   Specifies the table (e.g. FROM <table>)
        :param atts:    Specifies the attributes (e.g. SELECT <atts>)
        :param limit:   Specifies the number of entries in the result (e.g. LIMIT <limit>)
        :return:        Pandas DataFrame as result
        """

        if not atts:
            attrs_str = "*"
        else:
            attrs_str = ", ".join(atts)

        sql = f"SELECT {attrs_str} FROM {table} LIMIT {limit}"

        return self.get_data_from_query(query=sql)

    def get_data_from_query(self, query: str, **kwargs) -> pd.DataFrame:
        """
        Extracts data from the database based on a query.

        :param query:   SQL query for extracting data from the database
        :param kwargs:  Not supported yet
        :return:        Pandas DataFrame as result
        """

        try:
            df = pd.read_sql(query, con=self.conn)
            jsc.dataframe_to_json(df=df, title="postgres")

        except Exception as e:
            print(e)
            df = pd.DataFrame()

        finally:
            self._close_connection()

        return df

    def _close_connection(self) -> None:
        """Close the connection."""
        self.conn.close()
