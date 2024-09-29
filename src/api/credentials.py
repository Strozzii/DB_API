"""Stores the secrets"""

from src.api import constants as c
from src.api.login_objects import PostgresLogin, MongoLogin, NeoLogin


FINANCE_LOGIN = PostgresLogin(
    dbname="postgres",
    user="postgres",
    password="3589",
    host="localhost",
    port="5432"
)

RISK_MGMT_LOGIN = MongoLogin(
    host="mongodb://localhost:27017/",
    db="mongo",
    collection="risks"
)

TEAM_MAPPING_LOGIN = NeoLogin(
    host="bolt://localhost:7687",
    username="neo4j",
    password="normale_kartoffeln_auf_die_1",
)

POSTGRES_CREDS = {
    c.FINANCE: FINANCE_LOGIN
}

MONGO_CREDS = {
    c.RISKMGMT: RISK_MGMT_LOGIN
}

NEO_CREDS = {
    c.TEAMMAPPING: TEAM_MAPPING_LOGIN
}