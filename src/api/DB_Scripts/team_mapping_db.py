"""Module that deals specifically with communication with the team mapping database."""

from src.api.DB_Connections.neo import DataBase as Neo
from src.api.credentials import TEAM_MAPPING_LOGIN


class TeamsDB:
    """
    Represents an object which communicates with the team mapping database.

    attributes:
        db: Database object which communicates with the target database
    """

    def __init__(self) -> None:
        """Inits the Database object."""

        self.db = Neo()

    def get_all_project_leader(self) -> list[dict]:
        """
        Returns all employees who are responsible for a project.

        :return: List of dictionaries as result of the query and the result as a JSON-file
        """

        query = "MATCH (e:Employee)-[r:VERANTWORTLICH_FUER]-(p:Project) RETURN e, r, p"

        return self.db.get_data(query=query)
