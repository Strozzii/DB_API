"""This module sets up a PostgreSQL server."""

import random
from datetime import datetime, timedelta

import psycopg2
from psycopg2 import sql

from credentials import PostgresLogin as pl


def setup(number: int = 100):
    """
    Clears the existing Mongo database and populates it with random financial data.

    :param number: Number of test data (Default: 100)
    """

    conn = psycopg2.connect(
        dbname=pl.dbname,
        user=pl.user,
        password=pl.password,
        host=pl.host,
        port=pl.port
    )
    cur = conn.cursor()

    drop_table_query = sql.SQL("DROP TABLE IF EXISTS {table_name}").format(
        table_name=sql.Identifier('ausgaben')
    )
    cur.execute(drop_table_query)
    conn.commit()

    cur.execute('''
        CREATE TABLE IF NOT EXISTS ausgaben (
            id SERIAL PRIMARY KEY,
            department_id INTEGER,
            expense_date DATE,
            expense_type VARCHAR(255),
            description TEXT,
            amount NUMERIC(12, 2),
            currency VARCHAR(3),
            updated_at TIMESTAMP
        );
    ''')

    expense_types = ["Bürobedarf", "Reisekosten", "Verpflegung", "Unterhalt", "IT-Kosten", "Marketing", "Schulung",
                     "Consulting", "Sonstiges"]
    currencies = ["USD", "EUR", "GBP"]

    start_date = datetime(2023, 1, 1)

    for i in range(number):
        department_id = random.randint(1, 5)
        expense_date = start_date + timedelta(days=i)
        expense_type = random.choice(expense_types)
        description = f"Beispielbeschreibung {i + 1}" if random.random() > 0.3 else None
        amount = round(random.uniform(10, 10000), 2)
        currency = random.choice(currencies)
        updated_at = expense_date + timedelta(days=random.randint(0, 30))

        cur.execute(
            "INSERT INTO ausgaben (department_id, expense_date, expense_type, description, amount, currency, "
            "updated_at) VALUES (%s, %s, %s, %s, %s, %s, %s);",
            (department_id, expense_date, expense_type, description, amount, currency, updated_at)
        )

    conn.commit()
    cur.close()
    conn.close()
