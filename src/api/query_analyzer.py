from enum import Enum


class Syntax(Enum):
    NEO = "neo4j"
    POSTGRES = "postgresql"
    MONGO = "mongodb"


def analyze_query(query: str | dict):
    if isinstance(query, dict):
        return Syntax.MONGO

    if query.lower().startswith("select "):
        return Syntax.POSTGRES

    if query.lower().startswith("{"):
        return Syntax.MONGO

    if query.lower().startswith("match "):
        return Syntax.NEO

