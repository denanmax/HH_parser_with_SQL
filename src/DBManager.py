import psycopg2


class DBManager:
    """Класс для подключения и работы с postgres"""

    def __init__(self, database_name, params):
        self.params = params
        self.database_name = database_name
        self.connect = psycopg2.connect(dbname=database_name, **params)

    def get_companies_and_vacancies_count(self):
        """получает список всех компаний и количество вакансий у каждой компании."""
        with self.connect as conn:
            with conn.cursor() as cur:
                cur.execute("""
                select companies.name, count(vacancies.company_id) as vacancies_per_company
                from vacancies join companies on companies.company_id = vacancies.company_id
                group by companies.name
                """)

                return cur.fetchall()

    def get_all_vacancies(self):
        """получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию."""
        with self.connect as conn:
            with conn.cursor() as cur:
                cur.execute("""
                select companies.name, vacancies.name, vacancies.salary_min, vacancies.salary_max, vacancies.url
                from vacancies
                join companies on companies.company_id = vacancies.company_id
                order by companies.name
                """)

                return cur.fetchall()

    def get_avg_salary(self):
        """получает среднюю зарплату по вакансиям."""
        with self.connect as conn:
            with conn.cursor() as cur:
                cur.execute("""
                select (AVG(salary_min) + AVG(salary_max)) / 2
                from vacancies
                WHERE salary_min IS NOT NULL or salary_max IS NOT NULL
                """)

                return cur.fetchall()

    def get_vacancies_with_higher_salary(self):
        """получает список всех вакансий, у которых зарплата выше средней по всем вакансиям."""
        with self.connect as conn:
            with conn.cursor() as cur:
                cur.execute("""
                select *
                from vacancies
                WHERE salary_min > (SELECT AVG(salary_min) from vacancies) or salary_max > (SELECT AVG(salary_max) from vacancies)
                order by salary_min DESC
                """)

                return cur.fetchall()

    def get_vacancies_with_keyword(self, keyword):
        """получает список всех вакансий, в названии которых содержатся переданные в метод слова, например “python”."""
        with self.connect as conn:
            with conn.cursor() as cur:
                cur.execute(f"""
                SELECT * FROM vacancies 
                WHERE vacancies.name LIKE '%{keyword.title()}%'
                """)

                return cur.fetchall()
