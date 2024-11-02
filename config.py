import os
from configparser import ConfigParser


def config(filename="database.ini", section="postgresql"):
    '''Функция для подключения к БД'''

    filename = os.path.join(os.path.dirname(__file__), filename)
    parser = ConfigParser()

    parser.read(filename)
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]

    else:
        Exception('Section {0} is not found in the {1} file.'.format(section, filename))
        return None

    return db

if __name__ == '__main__':
    par = config()
    print(par)
