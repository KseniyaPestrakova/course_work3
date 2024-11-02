import requests


def get_10_employees():
    """ Функция для получения 10 работодателей с hh.ru"""

    list_employee = []
    for i in range(10):
        params = {"page": i, "per_page": 100}
        try:
            response = requests.get("https://api.hh.ru/employers", params=params).json()["items"]

            for employee in response:
                if employee["open_vacancies"] > 3:
                    if len(list_employee) < 10:
                        list_employee.append(
                            {'id': employee["id"], 'name': employee["name"], 'open_vacancies': employee["open_vacancies"]})
        except Exception:
            break

    sort_employee = sorted(list_employee, key=lambda x: x["open_vacancies"], reverse=True)

    return sort_employee


def get_vacancies(list_employee: list) -> list:
    """ Функция принимает список работодателей и выводит список с информацией по их вакансиям """

    vacancies_list = []
    for employee in list_employee:
        response = requests.get(f'https://api.hh.ru/vacancies?employer_id={employee["id"]}').json()["items"]
        for vacancy in response:
            vacancies_list.append({"employer": employee["id"],
                                   "vacancies": vacancy})
    return vacancies_list

if __name__ == '__main__':
    print(get_vacancies(get_10_employees()))
    # print(get_10_employees())
