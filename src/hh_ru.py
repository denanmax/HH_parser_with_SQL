import requests


class HHApi:
    def __init__(self, page=0):
        self.companies_id = [3529, 78638, 64174, 2748, 3672566,
                             3183420, 4625, 10066154, 1740, 4082, 238161]
        self.params = {
            "page": page,
            "pages": 3,
            "employer_id": self.companies_id,
            "only_with_salary": True,
            "per_page": 100,
            "area": 113
        }

    def get_vacancies(self):
        response = requests.get("https://api.hh.ru/vacancies", params=self.params)
        return response.json()["items"]

    def get_employers_data(self):
        employers_list = []

        for employer_id in self.companies_id:
            url = f"https://api.hh.ru/employers/{employer_id}"
            response = requests.get(url, params=self.params)
            employer_data = response.json()

            employer_info = {
                "id": employer_id,
                "name": employer_data.get("name"),
                "url": employer_data.get("alternate_url"),
            }

            employers_list.append(employer_info)

        return employers_list
