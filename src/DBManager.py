import psycopg2


class DBManager:
    """Класс для подключения и работы с postgres"""
    def __init__(self, database_name):
        self.database_name = database_name

    def get_companies_and_vacancies_count(self, database_name, params):
        """получает список всех компаний и количество вакансий у каждой компании."""
        with psycopg2.connect(dbname=database_name, **params) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                select companies.name, count(vacancies.company_id) as vacancies_per_company
                from vacancies join companies on companies.id = vacancies.company_id
                group by companies.name
                """)
                rows = cur.fetchall()
                for row in rows:
                    print(row)

    def get_all_vacancies(self, database_name, params):
        """получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию."""
        with psycopg2.connect(dbname=database_name, **params) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                select companies.name, vacancies.name, vacancies.salary_min, vacancies.salary_max, vacancies.url 
                from vacancies 
                join companies on companies.id = vacancies.company_id
                order by companies.name
                """)
                rows = cur.fetchall()
                for row in rows:
                    print(row)

    def get_avg_salary(self, database_name, params):
        """получает среднюю зарплату по вакансиям."""
        with psycopg2.connect(dbname=database_name, **params) as conn:
            with conn.cursor() as cur:
                cur.execute("""
            select (AVG(salary_min) + AVG(salary_max)) / 2
            from vacancies
            WHERE salary_min IS NOT NULL or salary_max IS NOT NULL
                """)
                rows = cur.fetchall()
                for row in rows:
                    print(row)

    def get_vacancies_with_higher_salary(self, database_name, params):
        """получает список всех вакансий, у которых зарплата выше средней по всем вакансиям."""
        with psycopg2.connect(dbname=database_name, **params) as conn:
            with conn.cursor() as cur:
                cur.execute("""
            select *
            from vacancies
            WHERE salary_min > (SELECT AVG(salary_min) from vacancies)
            order by salary_min
                """)
                rows = cur.fetchall()
                for row in rows:
                    print(row)

    def get_vacancies_with_keyword(self, database_name, params, keyword):
        """получает список всех вакансий, в названии которых содержатся переданные в метод слова, например “python”."""
        with psycopg2.connect(dbname=database_name, **params) as conn:
            with conn.cursor() as cur:
                cur.execute(f"""
            SELECT * FROM vacancies 
            WHERE vacancies.name LIKE '%{keyword.title()}%'
                """)
                rows = cur.fetchall()
                for row in rows:
                    print(row)

