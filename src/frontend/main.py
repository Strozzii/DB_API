"""This module is testing the API."""

import credentials as creds
from src.api.data_manager import DataManager
from src.frontend.applications.plot_interface import PlotInterface


class Main:
    """
    Represents an instance of a frontend software.

    Attributes:
            data: Instance of the API to communicate with the databases
            plot: Instance of a central application to plot images based on Pandas DataFrames
    """

    def __init__(self) -> None:
        """Inits the Main Class."""
        self.data = DataManager()
        self.plot = PlotInterface()

    def run(self) -> None:
        """Runs the script to simulate the frontend."""

        # Simple approach to call a specific database to get its data
        postgres_df = self.data.get_postgres_data(login=creds.FINANCE_LOGIN, table="ausgaben", atts=["id", "expense_type", "amount"], limit=9)
        mongo_df = self.data.get_mongo_data(login=creds.RISK_MGMT_LOGIN, atts=["title", "category"], limit=4)
        neo_df = self.data.get_neo_data(login=creds.TEAM_MAPPING_LOGIN, elements="(e : Employee)", atts=['e.name', 'e.id'])
        print(postgres_df.to_markdown())
        print(mongo_df.to_markdown())
        print(neo_df.to_markdown())

        # Generic approach to call any database that can handle this query
        df1 = self.data.get_data(login=creds.FINANCE_LOGIN, query="SELECT amount FROM ausgaben LIMIT 10")
        df2 = self.data.get_data(login=creds.RISK_MGMT_LOGIN, query={'risk_id': 1}, collection="risks")
        df3 = self.data.get_data(login=creds.TEAM_MAPPING_LOGIN, query="match (n)-[r]-(t) return n, r, t")
        print(df1.to_markdown())
        print(df2.to_markdown())
        print(df3.to_markdown())

        # Using template methods to extract data for a specific use case
        # expense_df1 = self.data.get_top_x_expenses(x=10)
        # expense_df2 = self.data.get_expenses_by_date(start="2023-02-05")
        # print(expense_df1.to_markdown())
        # print(expense_df2.to_markdown())


if __name__ == "__main__":
    main = Main()
    main.run()
