from config import config
from src.DBManager import DBManager
from src.api import get_10_employees
from src.utils import create_database, save_data_to_database


def main() -> None:
    print("Подключаемся к базе данных hh.ru\n")

    employees_list = get_10_employees()
    create_database('hh_ru')
    save_data_to_database(employees_list, 'hh_ru')

    params = config()
    data = DBManager('hh_ru', params)

    user_answer = input('Пожалуйста, введите номер действия, которое вас интересует:\n\n'
          '1. Получить список работодателей\n'
          '2. Получить полный список вакансий\n'
          '3. Узнать средний размер заработной платы по открытым вакансиям\n'
          '4. Получить список вакансий, у которых зарплата выше средней по всем вакансиям\n'
          '5. Получить список вакансий, в названии которых содержится определенное слово\n')
    try:
        if int(user_answer) == 1:
            result = data.get_companies_and_vacancies_count()
            for employer in result:
                print(f'У работодателя \'{employer[0]}\' открыто {employer[1]} вакансий')
        elif int(user_answer) == 2:
            result = data.get_all_vacancies()
            for vacancy in result:
                print(f'Работодатель: \'{vacancy[0]}\'\n'
                      f'Вакансия: {vacancy[1]}\n'
                      f'Зарплата: {vacancy[2]} руб.\n'
                      f'Ссылка на вакансию: {vacancy[3]}\n\n')
        elif int(user_answer) == 3:
            result = data.get_avg_salary()
            print(f'Средний размер заработной платы по открытым вакансиям составляет {result} рублей')
        elif int(user_answer) == 4:
            result = data.get_vacancies_with_higher_salary()
            for vacancy in result:
                print(f'Работодатель: \'{vacancy[0]}\'\n'
                      f'Вакансия: {vacancy[1]}\n'
                      f'Зарплата: {vacancy[2]} руб.\n'
                      f'Ссылка на вакансию: {vacancy[3]}\n\n')
        elif int(user_answer) == 5:
            word = input('Введите слово:')
            result = data.get_vacancies_with_keyword(word)
            for vacancy in result:
                print(f'Работодатель: \'{vacancy[0]}\'\n'
                      f'Вакансия: {vacancy[1]}\n'
                      f'Зарплата: {vacancy[2]} руб.\n'
                      f'Ссылка на вакансию: {vacancy[3]}\n\n')
    except ValueError:
        print('Действие не выбрано')


if __name__ == '__main__':
    print(main())
