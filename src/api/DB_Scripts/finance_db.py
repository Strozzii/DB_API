"""Takes care of the communication with the PostgreSQL database."""

from credentials import FINANCE_LOGIN
from src.api.DB_Connections.postgres import DataBase as Postgres


class FinanceDB:
    """Represents an object which communicates with the RiskMgmt database."""

    def __init__(self) -> None:
        """Inits the Database object."""

        self.db = Postgres(login=FINANCE_LOGIN)

    def get_expenses_by_date(self, start: str, end: str):

        base_query = "SELECT * FROM ausgaben WHERE expense_date "

        if start and not end:
            base_query += f">= '{start}'"

        elif not start and end:
            base_query += f"<= '{end}'"

        elif start and end:
            base_query += f"BETWEEN '{start}' AND '{end}'"

        else:
            raise ValueError("You need to provide at least one date as start or end!")

        return self.db.get_data_from_query(query=base_query)
