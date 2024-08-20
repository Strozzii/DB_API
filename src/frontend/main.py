"""This module is testing the API"""
from src.api.datacart import DataCart
from src.frontend.applications.plot_interface import PlotInterface


class Main:

    def __init__(self) -> None:
        self.data = DataCart()
        self.plot = PlotInterface()

    def run(self) -> None:
        postgres_df = self.data.get_postgres_data("ausgaben", [], limit=3)
        mongo_df = self.data.get_mongo_data("risks", [], limit=1)
        neo_df = self.data.get_neo_data("(e)", ['e.name', 'e.id'])

        print(mongo_df)

if __name__ == "__main__":
    main = Main()
    main.run()
