
import functions as fun
import DB as db
from tabulate import tabulate


'''
rabD - рабочее давление
rasD - расчетное давление
rabT - рабочая температура
rasT - расчетная температура
dNom - номинальный диаметр
skKorr - скорость коррозии
sreda - газ, пар или жидкость
gruppaSr - группа среды:
А - Токсичные, Класс 1, Класс 2, Класс 3
Б - Взрывопожароопасные, ГГ или СУГ, ЛВЖ, ГЖ
В - ТГ или НГ
'''


def pipe_digit_fun(message, param_name, result=' '):
    param = str(message.text)
    if fun.check_digit(param) != False:
        param = float(fun.zapyataya(param))
        # Работа с БД
        connection = db.create_connection('ORPD.sqlite', param_name)
        zapros = f'UPDATE pipe SET {param_name}={param} WHERE telegram_id={message.chat.id}'
        db.execute_query(connection, zapros, f'{param_name} внесение в БД')
        connection.close()
        # Конец работы с БД
        return result
    else:
        return None


def pipe_text_fun(message, param_name):
    param = str(message.text)
    # Работа с БД
    connection = db.create_connection('ORPD.sqlite', param_name)
    zapros = f'UPDATE pipe SET {param_name}="{param}" WHERE telegram_id={message.chat.id}'
    db.execute_query(connection, zapros, 'param_name внесение в БД')
    connection.close()
    # Конец работы с БД
    return True


def pipe_final_fun(message):
    connection = db.create_connection('ORPD.sqlite')
    q = f'SELECT * FROM pipe WHERE telegram_id={message.chat.id}'
    z ,= db.execute_read_query(connection, q)
    print(z)
    connection.close()