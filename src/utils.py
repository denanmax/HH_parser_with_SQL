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


def save_to_database(database_name, data, params):
    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        """Заполняем таблицу"""
        for vacancy in data:
            cur.execute("""
                SELECT * FROM companies WHERE id = %s;
            """, (vacancy['employer']['id'],))
            existing_company = cur.fetchone()

            if not existing_company:
                cur.execute("""
                    INSERT INTO companies(id, name, url)
                    VALUES (%s, %s, %s);
                """, (vacancy['employer']['id'], vacancy['employer']['name'],
                      vacancy['employer']['alternate_url']))

        for vacancy in data:
            salary_from = salary_to = None
            if vacancy['salary']:
                salary_from = vacancy['salary']['from']
                salary_to = vacancy['salary']['to']

            cur.execute("""
                INSERT INTO vacancies (name, company_id,salary_min, salary_max, url)
                VALUES (%s, %s, %s, %s, %s);
            """, (vacancy['name'], vacancy['employer']['id'],salary_from, salary_to,
                  vacancy['alternate_url']))

        conn.commit()
        conn.close()