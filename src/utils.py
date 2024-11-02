from typing import Any

import psycopg2

from config import config
from src.api import get_10_employees, get_vacancies


def create_database(database_name: str) -> Any:
    """Создание базы данных и таблиц для сохранения данных о работодателях и вакансиях."""
    params = config()
    conn = psycopg2.connect(dbname="postgres", **params)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f"DROP DATABASE IF EXISTS {database_name}")
    cur.execute(f"CREATE DATABASE {database_name}")

    conn.close()

    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        cur.execute(
            """
            CREATE TABLE employees (
                employer_id INTEGER PRIMARY KEY,
                company_name VARCHAR(255) NOT NULL,
                open_vacancies INTEGER
            )
        """
        )

    with conn.cursor() as cur:
        cur.execute(
            """
            CREATE TABLE vacancies (
                vacancy_id INT PRIMARY KEY,
                vacancy_name VARCHAR NOT NULL,
                vacancy_salary INT,
                vacancy_url TEXT,
                employer_id INT,
                FOREIGN KEY (employer_id) REFERENCES employees(employer_id)
            )
        """
        )

    conn.commit()
    conn.close()


def save_data_to_database(employees: list[dict[str, Any]], database_name: str) -> Any:
    """Сохранение данных о работодателях и вакансиях в базу данных."""
    params = config()
    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        for employer in employees:
            cur.execute(
                """
                INSERT INTO employees (employer_id, company_name, open_vacancies)
                VALUES (%s, %s, %s)
                """,
                (employer["id"], employer["name"], employer["open_vacancies"]),
            )

        vacancies_list = get_vacancies(employees)
        for employer in vacancies_list:
            if employer["vacancies"]["salary"]:
                cur.execute(
                    """
                    INSERT INTO vacancies (vacancy_id, vacancy_name, vacancy_salary, vacancy_url, employer_id)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (
                        employer["vacancies"]["id"],
                        employer["vacancies"]["name"],
                        employer["vacancies"]["salary"]["from"],
                        employer["vacancies"]["alternate_url"],
                        employer["employer"],
                    ),
                )
            else:
                cur.execute(
                    """
                    INSERT INTO vacancies (vacancy_id, vacancy_name, vacancy_salary, vacancy_url, employer_id)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (
                        employer["vacancies"]["id"],
                        employer["vacancies"]["name"],
                        0,
                        employer["vacancies"]["alternate_url"],
                        employer["employer"],
                    ),
                )
            cur.execute("""UPDATE vacancies set vacancy_salary=0 where vacancy_salary is null""")

    conn.commit()
    conn.close()


if __name__ == "__main__":
    # params = config()
    emp = get_10_employees()
    print(create_database("hh_ru"))
    print(save_data_to_database(emp, "hh_ru"))
