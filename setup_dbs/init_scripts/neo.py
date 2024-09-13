"""This module sets up a neo4j server."""

import random
from datetime import timedelta, datetime

import neo4j
from neo4j import GraphDatabase

from credentials import NeoLogin as nl


def setup():
    """Clears the existing neo database and populates it with random team mapping data."""

    uri = nl.host
    username = nl.username
    password = nl.password

    driver = GraphDatabase.driver(uri, auth=(username, password))

    with driver.session() as session:
        session.run("MATCH (n) DETACH DELETE n")
        session.write_transaction(create_test_data)


def random_date(start: datetime, end: datetime) -> datetime:
    """Returns a random date between a start and an end date."""
    return start + timedelta(days=random.randint(0, (end - start).days))


def random_role() -> str:
    """Returns a random role of an Employee."""
    roles = ["Developer", "Tester", "Architect"]
    return random.choice(roles)


def create_test_data(tx: neo4j.ManagedTransaction) -> None:
    """
    Creates test data for projects, teams and employees with relationships.

    :param tx: neo4j transaction unit
    """
    projects = [
        {"id": "p0001", "name": "Pearl", "budget": 10000},
        {"id": "p0002", "name": "Haven", "budget": 20000},
        {"id": "p0003", "name": "Lotus", "budget": 30000}
    ]

    teams = [
        {"id": "t1", "name": "Team Harbor"},
        {"id": "t2", "name": "Team Fade"},
        {"id": "t3", "name": "Team Viper"},
        {"id": "t4", "name": "Team Gekko"},
        {"id": "t5", "name": "Team Jett"},
        {"id": "t6", "name": "Team Deadlock"}
    ]

    employee_names = [
        "Anna Müller",
        "Bernd Schmidt",
        "Clara Meier",
        "David Braun",
        "Eva Fischer",
        "Franziska Hoffmann",
        "Georg Weber",
        "Hannah Koch",
        "Ian Schneider",
        "Julia Wagner",
        "Karl Schulz",
        "Laura Zimmermann",
        "Markus Lang",
        "Nina Richter",
        "Oliver Klein",
        "Petra Lange",
        "Quentin Berger",
        "Rita Peters",
        "Stefan Müller",
        "Tina Neumann",
        "Uwe Schwarz",
        "Vanessa Koch",
        "Walter Hartmann",
        "Xenia Günther",
        "Yvonne Schneider"
    ]

    employees = [
        {"id": f"e{i + 1}", "name": name, "Abteilung": f"Dept {i % 3}"}
        for i, name in enumerate(employee_names)
    ]

    for project in projects:
        tx.run(
            "CREATE (p:Project {id: $id, name: $name, budget: $budget})",
            id=project["id"], name=project["name"], budget=project["budget"]
        )

    for team in teams:
        tx.run(
            "CREATE (t:Team {id: $id, name: $name})",
            id=team["id"], name=team["name"]
        )

    for employee in employees:
        tx.run(
            "CREATE (e:Employee {id: $id, name: $name, Abteilung: $Abteilung})",
            id=employee["id"], name=employee["name"], Abteilung=employee["Abteilung"]
        )

    team_employees = {team['id']: [] for team in teams}
    for employee in employees:
        team_id = random.choice(teams)['id']
        team_employees[team_id].append(employee['id'])
        since_date = random_date(datetime(2022, 1, 1), datetime(2024, 6, 15))
        tx.run(
            "MATCH (e:Employee {id: $employee_id}), (t:Team {id: $team_id}) "
            "CREATE (e)-[:GEHOERT_ZU {since: $since_date}]->(t)",
            employee_id=employee['id'], team_id=team_id, since_date=since_date
        )

    project_teams = {}
    for project in projects:
        teams_for_project = random.sample(teams, k=random.randint(1, 2))
        project_teams[project['id']] = [team['id'] for team in teams_for_project]
        start_date = random_date(datetime(2022, 1, 1), datetime(2024, 6, 15))
        for team in teams_for_project:
            tx.run(
                "MATCH (t:Team {id: $team_id}), (p:Project {id: $project_id}) "
                "CREATE (t)-[:ARBEITEN_AN {start_date: $start_date}]->(p)",
                team_id=team['id'], project_id=project['id'], start_date=start_date
            )

    for project_id, team_ids in project_teams.items():
        responsible_employee = random.choice(employees)
        since_date = random_date(datetime(2022, 1, 1), datetime(2024, 6, 15))
        role = random_role()
        tx.run(
            "MATCH (e:Employee {id: $employee_id}), (p:Project {id: $project_id}) "
            "CREATE (e)-[:VERANTWORTLICH_FUER {role: $role, since: $since_date}]->(p)",
            employee_id=responsible_employee['id'], project_id=project_id, role=role, since_date=since_date
        )
