import psycopg2


def create_database(database_name, params):
    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f"DROP DATABASE IF EXISTS {database_name}")
    cur.execute(f"CREATE DATABASE {database_name}")

    conn.close()

    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        """создаем таблицу"""
        cur.execute("""
                        CREATE TABLE IF NOT EXISTS companies (
                        company_id SERIAL PRIMARY KEY,
                        name TEXT NOT NULL,
                        url TEXT NOT NULL
                        );
                    """)

    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS vacancies (
                    id INT PRIMARY KEY,
                    name TEXT NOT NULL,
                    company_id INT,
                    salary_min INT,
                    salary_max INT,
                    url VARCHAR(100) NOT NULL,
                    FOREIGN KEY (company_id) REFERENCES companies(company_id)
                );
        """)  # Создание таблицы синформацией о вакансиях (название, id компании, зп с/до, ссылка)

    conn.commit()
    conn.close()


def save_to_database_companies(database_name, data, params):
    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        for employer in data:
            cur.execute("""
                INSERT INTO companies (company_id, name, url)
                VALUES (%s, %s, %s)
            """, (
                employer["id"],
                employer["name"],
                employer["url"]
            ))
        conn.commit()
        conn.close()


def save_to_database_vacancies(database_name, data, params):
    conn = psycopg2.connect(dbname=database_name, **params)
    with conn.cursor() as cur:
        for vacancy in data:
            salary_from = salary_to = None
            if vacancy['salary']:
                salary_from = vacancy['salary']['from']
                salary_to = vacancy['salary']['to']
            cur.execute("""
                INSERT INTO vacancies (id, name, company_id, salary_min, salary_max, url)
                VALUES (%s, %s, %s, %s, %s, %s);
            """, (
                vacancy["id"],
                vacancy["name"],
                vacancy["employer"]["id"],
                salary_from,
                salary_to,
                vacancy["url"]
            ))

    conn.commit()
    conn.close()
