from src.DBManager import DBManager
from src.config import config
from src.hh_ru import HHApi
from src.utils import create_database, save_to_database


def main():
    companies_id = [
        3529,
        78638,
        64174,
        2748,
        3672566,
        3183420,
        4625,
        10066154,
        1740,
        4082,
        238161
    ]
    params = config()
    hh = HHApi()
    data = hh.get_vacancies(companies_id)
    database_name = input("Назовите БД")
    create_database(database_name, params)
    save_to_database(database_name, data, params)
    db = DBManager(database_name)
    input('список всех компаний и количество вакансий у каждой компании ')
    print(db.get_companies_and_vacancies_count(database_name, params))
    input('список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию ')
    print(db.get_all_vacancies(database_name, params))
    input('получает среднюю зарплату по вакансиям ')
    print(db.get_avg_salary(database_name, params))
    input('список всех вакансий, у которых зарплата выше средней по всем вакансиям ')
    print(db.get_vacancies_with_higher_salary(database_name, params))
    input('список всех вакансий, в названии которых содержатся переданные в метод слова ')
    keyword = input("введите слово ")
    print(db.get_vacancies_with_keyword(database_name, params, keyword))


if __name__ == '__main__':
    main()
