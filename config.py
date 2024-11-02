import os
from configparser import ConfigParser
from typing import Any


def config(filename: str ="database.ini", section: str ="postgresql") -> Any:
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
