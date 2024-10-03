"""Module that deals specifically with communication with the risk management database."""

from src.api.DB_Connections.mongo import DataBase as Mongo
from src.api.credentials import RISK_MGMT_LOGIN


class RiskDB:
    """
    Represents an object which communicates with the risk management database.

    attributes:
        db: Database object which communicates with the target database
    """

    def __init__(self):
        """Inits the Database object."""

        self.db = Mongo()

    def get_mitigation_plan(self, risk_id: str) -> list[dict]:
        """
        Returns the mitigation plan of a specific risk.

        :param risk_id: ID of the specific risk
        :return: List of dictionaries as result of the query and the result as a JSON-file
        """

        query = {
            "mitigation_plan": 1,
            "_id": 0
        }
        filter_dict = {"risk_id": risk_id}

        return self.db.get_data(query=query, filter_dict=filter_dict)
