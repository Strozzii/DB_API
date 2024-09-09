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

        # Targeted call of a method on a specific database type
        # postgres_finance_target_df = self.data.get_postgres_data(login=creds.FINANCE_LOGIN, table="ausgaben", atts=["id", "expense_type", "amount", "expense_date"], limit=9)
        # mongodb_risk_target_dict = self.data.get_mongo_data(login=creds.RISK_MGMT_LOGIN, atts=["title", "category"], limit=4)
        # neo4j_team_target_dict = self.data.get_neo_data(login=creds.TEAM_MAPPING_LOGIN, elements="(e : Employee)", atts=['e.name', 'e.id'])

        # Generic approach to call any database that can handle this query
        # postgres_finance_df = self.data.get_data(login=creds.FINANCE_LOGIN, query="SELECT amount FROM ausgaben LIMIT 10")
        # mongodb_risk_dict = self.data.get_data(login=creds.RISK_MGMT_LOGIN, query={'risk_id': 1})
        # neo4j_team_dict = self.data.get_data(login=creds.TEAM_MAPPING_LOGIN, query="match (n: Employee)-[r]-(t: Team) return n.name AS employee, r AS relation, t.name AS team")

        # Specific approach to target specific data from specific databases
        # finance_df = self.data.get_expenses_by_date(start="2023-02-15", end="2023-03-01")
        # risk_dict = self.data.get_mitigation_plan(risk_id="RISK-001")
        # team_dict = self.data.get_all_project_leader()




if __name__ == "__main__":
    main = Main()
    main.run()
