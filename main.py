from src.DBManager import DBManager
from src.config import config
from src.hh_ru import HHApi
from src.utils import create_database, save_to_database_companies, save_to_database_vacancies


def main():
    params = config()
    hh = HHApi()
    hh_employers = hh.get_employers_data()
    hh_vacancies = hh.get_vacancies()
    database_name = input("Назовите БД ")
    create_database(database_name, params)
    save_to_database_companies(database_name, hh_employers, params)
    save_to_database_vacancies(database_name, hh_vacancies, params)
    db = DBManager(database_name, params)
    while True:
        print("""
                1 - список всех компаний и количество вакансий у каждой компании
                2 - список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию
                3 - получает среднюю зарплату по вакансиям
                4 - список всех вакансий, у которых зарплата выше средней по всем вакансиям
                5 - список всех вакансий, в названии которых содержатся переданные в метод слова
                stop/стоп - Остановить\n""")

        user_input = input("Ваш выбор:").lower()

        if user_input == '1':
            input('Вывести список всех компаний и количество вакансий у каждой компании?')
            for vacancy in db.get_companies_and_vacancies_count():
                print(vacancy)
        elif user_input == '2':
            input(
                'Вывести список всех вакансий с указанием названия компании, '
                'названия вакансии и зарплаты и ссылки на вакансию?')
            for vacancy in db.get_all_vacancies():
                print(vacancy)
        elif user_input == '3':
            input('Вывести получает среднюю зарплату по вакансиям?')
            for vacancy in db.get_avg_salary():
                print(vacancy)
        elif user_input == '4':
            input('Вывести список всех вакансий, у которых зарплата выше средней по всем вакансиям?')
            for vacancy in db.get_vacancies_with_higher_salary():
                print(vacancy)
        elif user_input == '5':
            input('Вывести список всех вакансий, в названии которых содержатся переданные в метод слова?')
            keyword = input("введите слово ")
            for vacancy in db.get_vacancies_with_keyword(keyword):
                print(vacancy)
        elif user_input == 'stop' or user_input == 'стоп':
            print("ДОСВИДАНИЯ!!!")
            break
        else:
            print("Некорректный ввод!")


if __name__ == '__main__':
    main()
