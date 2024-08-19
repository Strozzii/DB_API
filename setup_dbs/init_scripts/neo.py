"""This module sets up a neo4j server"""

import random
from datetime import datetime, timedelta

from neo4j import GraphDatabase


def setup(number: int = 100):
    """
    Clears the existing neo4j database and populates it with test financial data

    :param number: Number of test data (Default: 100)
    """

    print(f"Starting {__name__} ...")

    # Create DB instance
    uri = "bolt://localhost:7687"
    driver = GraphDatabase.driver(uri, auth=("neo4j", "normale_kartoffeln_auf_die_1"))

    def create_ausgabe(tx, department_id, expense_date, expense_type, description, amount, currency, updated_at):
        """
        Sub-function to create a node in neo4j

        :param tx: Transaction unit
        :param department_id: Reference to the department
        :param expense_date: Date of expense
        :param expense_type: Type of expense
        :param description: Description of the expense (optional, for more details)
        :param amount: Amount of the expense
        :param currency: Currency of the expense (Supported are: USD, EUR and GBP)
        :param updated_at: Timestamp of when the node was last updated
        """

        tx.run("""
        CREATE (a:Ausgabe {
            department_id: $department_id, 
            expense_date: $expense_date, 
            expense_type: $expense_type, 
            description: $description, 
            amount: $amount, 
            currency: $currency,
            updated_at: $updated_at
        })
        """,
               department_id=department_id,
               expense_date=expense_date,
               expense_type=expense_type,
               description=description,
               amount=amount,
               currency=currency,
               updated_at=updated_at)

    with driver.session() as session:

        # Clear DB
        session.run("MATCH ()-[r]->() DELETE r")
        session.run("MATCH (n) DELETE n")

        # Setup DB
        expense_types = ["Bürobedarf", "Reisekosten", "Verpflegung", "Unterhalt", "IT-Kosten", "Marketing", "Schulung",
                         "Consulting", "Sonstiges"]
        currencies = ["USD", "EUR", "GBP"]

        # Test data has timestamp starting from 01.01.2023
        start_date = datetime(2023, 1, 1)

        for i in range(number):
            department_id = random.randint(1, 5)
            expense_date = (start_date + timedelta(days=i)).isoformat()
            expense_type = random.choice(expense_types)
            description = f"Beispielbeschreibung {i + 1}" if random.random() > 0.3 else None
            amount = round(random.uniform(10, 10000), 2)
            currency = random.choice(currencies)
            updated_at = (datetime.fromisoformat(expense_date) + timedelta(days=random.randint(0, 30))).isoformat()

            session.write_transaction(create_ausgabe, department_id, expense_date, expense_type, description, amount,
                                      currency, updated_at)

    driver.close()

    print(f"Finished {__name__} !")
