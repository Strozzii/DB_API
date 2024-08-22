"""Central applications which works as a wrapper for matplotlib."""

import pandas as pd
from matplotlib import pyplot as plt


class PlotInterface:
    """Handles all plot creations."""

    def make_bar_graph(self, df: pd.DataFrame, x: str, y: str, title: str) -> None:
        """
        Shows a plot as a bar graph based on a Pandas DataFrame.

        :param x:       x-axes values
        :param y:       y-axes values
        :param df:      Pandas DataFrames with data to show
        :param title:   Label above the plot to identify the plot
        """

        # The figure and axes objects need to be deleted due to overlapping results
        self._destroy()

        # Plotting
        plt.bar(x=df[x], height=df[y])

        # Plot configuration
        plt.title(title)
        plt.xticks(rotation=45, fontsize=6)
        plt.subplots_adjust(bottom=0.15)

        plt.show()

    @staticmethod
    def _destroy() -> None:
        """Deletes Pyplots figure and axes objects and closes active Pyplot windows."""

        plt.cla()
        plt.clf()
        plt.close()
