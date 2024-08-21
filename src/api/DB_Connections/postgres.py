import pandas as pd
import psycopg2

import credentials as creds


class DataBase:

    def __init__(self) -> None:
        self.conn = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password=creds.POSTGRES_PASSWORD,
            host="localhost",
            port="5432"
        )

    def get_data(self, table: str, atts: list, limit: int) -> pd.DataFrame:

        if not atts:
            attrs_str = "*"
        else:
            attrs_str = ", ".join(atts)

        sql = f"SELECT {attrs_str} FROM {table} LIMIT {limit}"

        try:
            df = pd.read_sql(sql, con=self.conn)
        except Exception as e:
            print(e)
            df = pd.DataFrame()

        return df

    def get_data_from_query(self, query):
        try:
            df = pd.read_sql(query, con=self.conn)
        except Exception as e:
            print(e)
            df = pd.DataFrame()

        return df
