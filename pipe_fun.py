
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

def pipe_rabD_fun(message, result=' '):
    rabD = str(message.text)
    if fun.check_digit(rabD) != False:
        rabD = float(fun.zapyataya(rabD))
        # Работа с БД
        connection = db.create_connection('ORPD.sqlite', '1')
        zapros = f'UPDATE pipe SET rabD={rabD} WHERE telegram_id={message.chat.id}'
        db.execute_query(connection, zapros, 'Рабочее давление внесение в БД')
        connection.close()
        # Конец работы с БД
        return result
    else:
        return None


def pipe_rasD_fun(message, result=' '):
    rasD = str(message.text)
    if fun.check_digit(rasD) != False:
        rasD = float(fun.zapyataya(rasD))
        # Работа с БД
        connection = db.create_connection('ORPD.sqlite', '2')
        zapros = f'UPDATE pipe SET rasD={rasD} WHERE telegram_id={message.chat.id}'
        db.execute_query(connection, zapros, 'Расчетное давление внесение в БД')
        connection.close()
        # Конец работы с БД
        return result
    else:
        return None

def pipe_rabT_fun(message, result=' '):
    rabT = str(message.text)
    if fun.check_digit(rabT) != False:
        rabT = float(fun.zapyataya(rabT))
        # Работа с БД
        connection = db.create_connection('ORPD.sqlite', '3')
        zapros = f'UPDATE pipe SET rabT={rabT} WHERE telegram_id={message.chat.id}'
        db.execute_query(connection, zapros, 'Рабочая температура внесение в БД')
        connection.close()
        # Конец работы с БД
        return result
    else:
        return None
    
def pipe_rasT_fun(message, result=' '):
    rasT = str(message.text)
    if fun.check_digit(rasT) != False:
        rasT = float(fun.zapyataya(rasT))
        # Работа с БД
        connection = db.create_connection('ORPD.sqlite', '3')
        zapros = f'UPDATE pipe SET rasT={rasT} WHERE telegram_id={message.chat.id}'
        db.execute_query(connection, zapros, 'Расчетная температура внесение в БД')
        connection.close()
        # Конец работы с БД
        return result
    else:
        return None
    
def pipe_nomD_fun(message, result=' '):
    nomD = str(message.text)
    if fun.check_digit(nomD) != False:
        nomD = float(fun.zapyataya(nomD))
        # Работа с БД
        connection = db.create_connection('ORPD.sqlite', '4')
        zapros = f'UPDATE pipe SET nomD={nomD} WHERE telegram_id={message.chat.id}'
        db.execute_query(connection, zapros, 'Номинальный диаметр внесение в БД')
        connection.close()
        # Конец работы с БД
        return result
    else:
        return None
    
def pipe_skKorr_fun(message, result=' '):
    skKorr = str(message.text)
    if fun.check_digit(skKorr) != False:
        skKorr = float(fun.zapyataya(skKorr))
        # Работа с БД
        connection = db.create_connection('ORPD.sqlite', '4')
        zapros = f'UPDATE pipe SET skKorr={skKorr} WHERE telegram_id={message.chat.id}'
        db.execute_query(connection, zapros, 'Скорость коррозии внесение в БД')
        connection.close()
        # Конец работы с БД
        return result
    else:
        return None

def pipe_sreda_fun(message):
    sreda = str(message.text)
    # Работа с БД
    connection = db.create_connection('ORPD.sqlite', '5')
    zapros = f'UPDATE pipe SET sreda="{sreda}" WHERE telegram_id={message.chat.id}'
    db.execute_query(connection, zapros, 'Тип среды внесение в БД')
    connection.close()
    # Конец работы с БД
    return True

def pipe_category_fun(message):
    category = str(message.text)
    # Работа с БД
    connection = db.create_connection('ORPD.sqlite', '6')
    zapros = f'UPDATE pipe SET pipe_category="{category}" WHERE telegram_id={message.chat.id}'
    db.execute_query(connection, zapros, 'Категория среды внесение в БД')
    connection.close()
    # Конец работы с БД
    return True