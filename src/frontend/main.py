"""This module is testing the API"""
from src.api.datacart import DataCart
from src.frontend.applications.plot_interface import PlotInterface


class Main:

    def __init__(self) -> None:
        self.data = DataCart()
        self.plot = PlotInterface()

    def run(self) -> None:
        # Simple approach to call a specific database to get its data
        postgres_df = self.data.get_postgres_data("ausgaben", [], limit=3)
        mongo_df = self.data.get_mongo_data("risks", [], limit=1)
        neo_df = self.data.get_neo_data("(e)", ['e.name', 'e.id'])

        # Generic approach to call any database that can handle this query
        df1 = self.data.get_data("SELECT amount FROM ausgaben LIMIT 10")
        df2 = self.data.get_data({'risk_id': 1}, collection="risks")
        df3 = self.data.get_data("match (n)-[r]-(t) return n, r, t")

        print(df3)


if __name__ == "__main__":
    main = Main()
    main.run()
