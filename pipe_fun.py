
import functions as fun
import DB as db
from tabulate import tabulate

'''
rabD - рабочее давление
rasD - расчетное давление
rabT - рабочая температура
rasT - расчетная температура
dNom - номинальный диаметр
sreda - газ, пар или жидкость
skKorr - скорость коррозии
gruppaSr - группа среды:
А - Токсичные, Класс 1, Класс 2, Класс 3
Б - Взрывопожароопасные, ГГ или СУГ, ЛВЖ, ГЖ
В - ТГ или НГ
'''


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
        db.execute_query(connection, zapros, 'Расчетное давление внесение в БД')
        connection.close()
        # Конец работы с БД
        return result
    else:
        return None