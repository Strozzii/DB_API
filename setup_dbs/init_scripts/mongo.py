"""This module sets up a MongoDB server"""

import random
from datetime import datetime, timedelta

from pymongo import MongoClient


def setup(number: int = 100) -> None:
    """
    Clears the existing Mongo database and populates it with test financial data

    :param number: Number of test data (Default: 100)
    """

    print(f"Starting {__name__} ...")

    # Create DB instance
    client = MongoClient("mongodb://localhost:27017/")
    db = client["mongo"]
    collection = db["ausgaben"]

    # Clear database
    collection.drop()

    # Setup part
    expense_types = ["Bürobedarf", "Reisekosten", "Verpflegung", "Unterhalt", "IT-Kosten", "Marketing", "Schulung",
                     "Consulting", "Sonstiges"]
    currencies = ["USD", "EUR", "GBP"]

    # Test data has timestamp starting from 01.01.2023
    start_date = datetime(2023, 1, 1)

    test_data = []
    for i in range(number):
        department_id = random.randint(1, 5)
        expense_date = start_date + timedelta(days=i)
        expense_type = random.choice(expense_types)
        description = f"Beispielbeschreibung {i + 1}" if random.random() > 0.3 else None
        amount = round(random.uniform(10, 10000), 2)
        currency = random.choice(currencies)
        updated_at = expense_date + timedelta(days=random.randint(0, 30))

        test_data.append({
            "department_id": department_id,
            "expense_date": expense_date,
            "expense_type": expense_type,
            "description": description,
            "amount": amount,
            "currency": currency,
            "updated_at": updated_at
        })

    collection.insert_many(test_data)

    print(f"Finished {__name__} !")
