"""This module is testing the API"""
import pandas as pd

from src.api.DataCart import DataCart
from src.frontend.applications.plot_interface import PlotInterface


class Main:

    def __init__(self) -> None:
        self.data = DataCart()
        self.plot = PlotInterface()

    def run(self) -> None:
        self.data.fetch_all_data()
        bulky_dataframe = self.data.load(is_bulk=True)

        for key, df in bulky_dataframe.items():
            self.plot.make_bar_graph(df=df[-7:], title=key)

        for df in bulky_dataframe.values():
            df["expense_date"] = pd.to_datetime(df["expense_date"])
        df = pd.concat(bulky_dataframe.values()).groupby(["expense_date"], as_index=False)["amount"].sum()
        self.plot.make_bar_graph(df=df[-7:], title="all")

if __name__ == "__main__":
    main = Main()
    main.run()
