- Создаем таблицу компаний

CREATE TABLE IF NOT EXISTS companies (
id SERIAL PRIMARY KEY,
name TEXT NOT NULL,
url TEXT NOT NULL
);

- Создаем таблицу вакансий

CREATE TABLE IF NOT EXISTS vacancies (
id SERIAL PRIMARY KEY,
name TEXT NOT NULL,
company_id INT REFERENCES companies(id),
salary_min INT,
salary_max INT,
url TEXT NOT NULL
);

- Заполняем таблицы
-компаний
INSERT INTO companies(id, name, url)
VALUES (%s, %s, %s)
ON CONFLICT DO NOTHING
-вакансий
INSERT INTO vacancies (name, company_id, salary_min, salary_max, url)
VALUES (%s, %s, %s, %s, %s)

-получает среднюю зарплату по вакансиям

select AVG(salary_min)
from vacancies
WHERE salary_min > 1

-получает список всех вакансий, у которых зарплата выше средней по всем вакансиям

select *
from vacancies
WHERE salary_min > (SELECT AVG(salary_min) from vacancies)
order by salary_min

-получает список всех вакансий, в названии которых содержатся переданные в метод слова, например “python”

SELECT * FROM vacancies
WHERE vacancies.name LIKE '%{keyword.title()}%'