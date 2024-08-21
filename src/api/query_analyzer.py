"""Module that analyses database queries."""

from enum import Enum


class Syntax(Enum):
    """Enumeration that represents a database syntax."""
    NEO = "neo4j"
    POSTGRES = "postgresql"
    MONGO = "mongodb"


def analyze_query(query: str | dict) -> Syntax:
    """
    Analyses a database query based on its syntax.

    :param query:   Database query to be analysed
    :return:        Syntax object, matching the query syntax
    """
    if isinstance(query, dict):
        return Syntax.MONGO

    if query.lower().startswith("select "):
        return Syntax.POSTGRES

    if query.lower().startswith("{"):
        return Syntax.MONGO

    if query.lower().startswith("match "):
        return Syntax.NEO

