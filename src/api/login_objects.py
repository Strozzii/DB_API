"""Dataclasses to have a uniform way to connect to supported databases."""

from dataclasses import dataclass


@dataclass
class BaseLogin:
    host: str


@dataclass
class PostgresLogin(BaseLogin):
    dbname: str
    user: str
    password: str
    port: str


@dataclass
class MongoLogin(BaseLogin):
    db: str
    collection: str


@dataclass
class NeoLogin(BaseLogin):
    username: str
    password: str
