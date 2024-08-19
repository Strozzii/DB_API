"""This module is testing the API"""

from src.api.DataCart import DataCart


class Main:

    def __init__(self) -> None:
        self.data = DataCart()

    def run(self) -> None:
        self.data.fetch_all_data()
        bulky_dataframe = self.data.load(is_bulk=True)

        for df in bulky_dataframe.values():
            print(df)


if __name__ == "__main__":
    main = Main()
    main.run()
