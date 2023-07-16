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
                        company_id INT,
                        salary_min INT,
                        salary_max INT,
                        url TEXT NOT NULL,
                        FOREIGN KEY (company_id) REFERENCES companies(id)
    );
                    """)

    conn.commit()
    conn.close()



def save_to_database_companies(database_name, data, params):
    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        for company in data:
            cur.execute("""
                INSERT INTO companies(id, name, url)
                VALUES (%s, %s, %s)
                ON CONFLICT (id) DO NOTHING""",
                (company['employer']['id'], company['employer']['name'], company['employer']['alternate_url']))
        conn.commit()
        conn.close()

def save_to_database_vacancies(database_name, data, params):
    conn = psycopg2.connect(dbname=database_name, **params)
    with conn.cursor() as cur:
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