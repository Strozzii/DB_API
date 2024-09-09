"""Takes care of the communication with the PostgreSQL database."""
from typing import Any

import pandas as pd
from pymongo import MongoClient

from src.api.DB_Connections.mongo import DataBase as Mongo
from credentials import RISK_MGMT_LOGIN


class RiskDB:
    """Represents an object which communicates with the RiskMgmt database."""

    def __init__(self):
        """Inits the Database object."""

        self.db = Mongo(login=RISK_MGMT_LOGIN)

    def get_mitigation_plan(self, risk_id: str) -> pd.DataFrame:

        query = {
            "mitigation_plan": 1,
            "_id": 0
        }
        filter_dict = {"risk_id": risk_id}

        return self.db.get_data_from_query(query=query, filter_dict=filter_dict)
