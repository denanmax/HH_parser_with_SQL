import psycopg2

from config import config
from src.hh_ru import HHApi


def create_database(database_name, params):
    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f"DROP DATABASE IF EXISTS {database_name}")
    cur.execute(f"CREATE DATABASE {database_name}")

    conn.close()

    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        cur.execute("""
                        CREATE TABLE employers (
                            id INTEGER PRIMARY KEY,
                            name varchar(100) NOT NULL,
                            emp_url varchar (100) NOT NULL
                        )
                    """)

    with conn.cursor() as cur:
        cur.execute("""
                        CREATE TABLE IF NOT EXISTS vacancies (
                        name TEXT NOT NULL,
                        company_id INT REFERENCES employers(id),
                        salary_min INT,
                        salary_max INT,
                        url TEXT NOT NULL
                        );
                    """)

        conn.commit()
        conn.close()


def save_to_database(database_name, data, params):
    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        for company in data:
            cur.execute("""
                                INSERT INTO employers(id, name, emp_url)
                                VALUES (%s, %s, %s)
                             """,
                        (company['employer']['id'], company['employer']['name'], company['employer']['alternate_url']))

        for item in data:
            salary_from = salary_to = None
            if item['salary']:
                salary_from = item['salary']['from']
                salary_to = item['salary']['to']
            cur.execute(f"""
                        INSERT INTO vacancies (name, company_id, salary_min, salary_max, url) 
                        VALUES (%s, %s, %s, %s, %s)""", (
                item['name'], item['employer']['id'], salary_from, salary_to, item['alternate_url']
            )
                        )
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
database_name = "один"
create_database(database_name, params)
save_to_database(database_name, data, params)
