"""Module that deals specifically with communication with the financial database."""

import pandas as pd

from src.api.credentials import FINANCE_LOGIN
from src.api.DB_Connections.postgres import DataBase as Postgres


class FinanceDB:
    """
    Represents an object which communicates with the financial database.

    attributes:
        db: Database object which communicates with the target database
    """

    def __init__(self) -> None:
        """Inits the Database object."""

        self.db = Postgres()

    def get_expenses_by_date(self, start: str = "", end: str = "") -> pd.DataFrame:
        """
        Returns the expenses in a specific time interval. It's possible to leave an argument empty.

        :param start:   Datetime object representing the left interval limit
        :param end:     Datetime object representing the right interval limit
        :return:        Pandas DataFrame as result of the query and the result as a JSON-file
        """

        base_query = "SELECT * FROM ausgaben WHERE expense_date "

        if start and not end:
            base_query += f">= '{start}'"

        elif not start and end:
            base_query += f"<= '{end}'"

        elif start and end:
            base_query += f"BETWEEN '{start}' AND '{end}'"

        else:
            raise ValueError("You need to provide at least one date as start or end!")

        return self.db.get_data(query=base_query)
