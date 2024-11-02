import psycopg2

from config import config


class DBManager:
    def __init__(self, database_name: str, params: dict):
        self.params = params
        self.conn = psycopg2.connect(dbname=database_name, **params)
        self.cur = self.conn.cursor()

    def get_companies_and_vacancies_count(self):
        self.cur.execute("SELECT company_name, open_vacancies from employees")

        return self.cur.fetchall()

    def get_all_vacancies(self):
        self.cur.execute(
            "SELECT company_name, vacancy_name, vacancy_salary, vacancy_url "
            "from employees "
            "join vacancies on employees.employer_id = vacancies.employer_id")

        return self.cur.fetchall()

    def get_avg_salary(self):
        self.cur.execute("select AVG(vacancy_salary) from vacancies")
        return round(float(self.cur.fetchall()[0][0]),2)

    def get_vacancies_with_higher_salary(self):
        self.cur.execute("select * from vacancies where vacancy_salary > (select AVG(vacancy_salary) from vacancies)")
        return self.cur.fetchall()

    def get_vacancies_with_keyword(self, word):
        self.cur.execute(f"select * from vacancies where vacancy_name like '%{word}%'")
        return self.cur.fetchall()


if __name__ == '__main__':
    par = config()
    exp = DBManager('hh_ru', par)
    res = exp.get_vacancies_with_keyword('менеджер')
    print(res)
