import requests


class HHApi:
    def __init__(self):
        self.url = "https://api.hh.ru/vacancies"

    def get_vacancies(self, emp_id):
        """Метод получения данных о вакансиях с сайта hh.ru по id компании"""

        params = {
            "employer_id": list(emp_id),
            "per_page": 100,
            "area": 113,
        }
        headers = {
            "User-Agent": "49336138",
        }

        response = requests.get(self.url, params=params, headers=headers).json()['items']

        return response
