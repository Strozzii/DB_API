"""This module is testing the API."""

from src.api.data_dispenser import DataDispenser
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
        self.data = DataDispenser()
        self.plot = PlotInterface()

    def run(self) -> None:
        """Runs the script to simulate the frontend."""

        # Simple approach to call a specific database to get its data
        postgres_df = self.data.get_postgres_data(table="ausgaben", atts=[], limit=3)
        mongo_df = self.data.get_mongo_data(collection="risks", atts=[], limit=1)
        neo_df = self.data.get_neo_data(elements="(e)", atts=['e.name', 'e.id'])

        # Generic approach to call any database that can handle this query
        df1 = self.data.get_data(query="SELECT amount FROM ausgaben LIMIT 10")
        df2 = self.data.get_data(query={'risk_id': 1}, collection="risks")
        df3 = self.data.get_data(query="match (n)-[r]-(t) return n, r, t")

        # Using template methods to extract data for a specific use case
        expense_df1 = self.data.get_top_x_expenses(x=10)
        expense_df2 = self.data.get_expenses_by_date(start="2023-02-05")

        print(expense_df2.to_markdown())


if __name__ == "__main__":
    main = Main()
    main.run()
