import psycopg2

from config import config
from hh_ru import HHApi


def create_database(db_name, params):
    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f"DROP DATABASE IF EXISTS {db_name}")
    cur.execute(f"CREATE DATABASE {db_name}")

    conn.close()

    conn = psycopg2.connect(dbname=db_name, **params)

    with conn.cursor() as cur:
        cur.execute("""
                        CREATE TABLE IF NOT EXISTS companies (
                        id SERIAL PRIMARY KEY,
                        name TEXT NOT NULL,
                        url TEXT NOT NULL
                        );
                    """)

    with conn.cursor() as cur:
        cur.execute("""
                        CREATE TABLE IF NOT EXISTS vacancies (
                        id SERIAL PRIMARY KEY,
                        name TEXT NOT NULL,
                        company_id INT REFERENCES companies(id),
                        salary_min INT,
                        salary_max INT,
                        url TEXT NOT NULL
                        );
                    """)

    conn.commit()
    conn.close()


def save_to_database(db_name, data, params):
    conn = psycopg2.connect(dbname=db_name, **params)

    with conn.cursor() as cur:
        for vacancy in data:
            cur.execute("""
                                            INSERT INTO companies(id, name, url)
                                            VALUES (%s, %s, %s)
                                            ON CONFLICT DO NOTHING
                                         """,
                        (vacancy['employer']['id'], vacancy['employer']['name'], vacancy['employer']['alternate_url']))

        for vacancy in data:
            salary_from = salary_to = None
            if vacancy['salary']:
                salary_from = vacancy['salary']['from']
                salary_to = vacancy['salary']['to']
            cur.execute("""
                 INSERT INTO vacancies (name, company_id, salary_min, salary_max, url)
                 VALUES (%s, %s, %s, %s, %s)
                 """,
                        (vacancy['name'], vacancy['employer']['id'], salary_from, salary_to,
                         vacancy['alternate_url']))

        conn.commit()
        conn.close()


companies_id = [
            3529,
            78638,
            64174,
            2748,
            3672566,
            3183420,
            4625,
            106571,
            1740,
            4300631
]
params = config()
hh = HHApi()
data = hh.get_vacancies(companies_id)
db_name = "baza"
create_database(db_name, params)
save_to_database(db_name, data, params)

