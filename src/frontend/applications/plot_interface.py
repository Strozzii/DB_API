"""Central applications which works as a wrapper for matplotlib"""
import pandas as pd
from matplotlib import pyplot as plt


class PlotInterface:

    def make_bar_graph(self, df: pd.DataFrame, title: str) -> None:
        self._destroy()

        plt.bar(x=df["expense_date"], height=df["amount"])
        plt.title(title)
        plt.xticks(rotation=45, fontsize=6)
        plt.subplots_adjust(bottom=0.15)
        plt.show()

    @staticmethod
    def _destroy() -> None:
        plt.cla()
        plt.clf()
        plt.close()
