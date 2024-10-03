"""This module is testing the API."""

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

        # Targeted call of a method on a specific database type
        # postgres_finance_target_df = self.data.get_postgres_data(table="ausgaben", atts=["id", "expense_type", "amount", "expense_date"], limit=9)
        # mongodb_risk_target_dict = self.data.get_mongo_data(atts=["title", "category", "reported_by"], limit=4)
        # neo4j_team_target_dict = self.data.get_neo_data(elements="(e : Employee)", atts=['e.name', 'e.id'])

        # self.plot.make_bar_graph(postgres_finance_target_df, "expense_date", "amount", "Kosten der letzten 9 Tage")

        # Generic approach to call any database that can handle this query
        # postgres_finance_df = self.data.get_data(query="SELECT * FROM ausgaben LIMIT 10")
        # mongodb_risk_dict = self.data.get_data(query={'risk_id': 1})
        # neo4j_team_dict = self.data.get_data(query="MATCH (e:Employee)-[r:GEHOERT_ZU]->(t:Team) RETURN e, r, t")

        # Specific approach to target specific data from specific databases
        # finance_df = self.data.get_expenses_by_date(start="2023-02-15", end="2023-03-01")
        # risk_dict = self.data.get_mitigation_plan(risk_id="RISK-001")
        # team_dict = self.data.get_all_project_leader()


if __name__ == "__main__":
    main = Main()
    main.run()
