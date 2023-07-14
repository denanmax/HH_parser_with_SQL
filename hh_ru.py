import requests


class HHApi:
    def __init__(self):
        self.url = "https://api.hh.ru/vacancies"

    def get_vacancies(self, emp_id):
        """
            Метод получения данных о вакансиях с сайта hh.ru по id компании
            param emp_id: id компании для поиска вакансий
            return: список со словарями
        """

        params = {
            "employer_id": list(emp_id),
            "per_page": 100,
            "area": 113,
            "only_with_salary": True

        }

        responce = requests.get(self.url, params=params).json()['items']

        return responce
