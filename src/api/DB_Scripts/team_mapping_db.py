"""Takes care of the communication with the PostgreSQL database."""

import psycopg2
import pandas as pd
from neo4j import GraphDatabase

from src.api.DB_Connections.neo import DataBase as Neo
from credentials import TEAM_MAPPING_LOGIN


class TeamsDB:
    """Represents an object which communicates with the RiskMgmt database."""

    def __init__(self) -> None:
        """Inits the Database object."""

        self.db = Neo(login=TEAM_MAPPING_LOGIN)

    def get_all_project_leader(self):

        query = "MATCH (e:Employee)-[:VERANTWORTLICH_FUER]-(p:Project) RETURN e"

        return self.db.get_data_from_query(query=query)
