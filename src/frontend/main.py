"""This module is testing the API"""
import pandas as pd

from src.api.datacart import DataCart
from src.frontend.applications.plot_interface import PlotInterface


class Main:

    def __init__(self) -> None:
        self.data = DataCart()
        self.plot = PlotInterface()

    def run(self) -> None:
        postgres_df = self.data.get_postgres_data("ausgaben", ['expense_date', 'amount'], limit=3)
        mongo_df = self.data.get_mongo_data("risks", ['risk_id', 'title', 'risk_score'], limit=3)
        neo_df = self.data.get_neo_data("(e)", ['e.name', 'e.id'])
        print(neo_df)


if __name__ == "__main__":
    main = Main()
    main.run()
