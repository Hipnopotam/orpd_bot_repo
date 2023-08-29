
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
    # (8, 48691773, 'Alexey N.', '1.0', '2.0', '3.0', '4.0', '5.0', 'Пар', '6.0', 'ТГ или НГ', None, 'no_active')
    _, user_id, user_name, rabD, rasD, rabT, rasT, nomD, sreda, skKorr, pipe_category, *_ = z
    result = f'''
Трубопровод

Рабочее давление - {rabD} МПа,
Расчетное давление - {rasD} МПа,
Рабочая температура - {rabT} C,
Расчетная температура - {rasT} C,
Номинальный диаметр - {nomD} мм,
Скорость коррозии - {skKorr} мм/год,
Тип среды - {sreda},
Категория среды - {pipe_category}
'''
    connection.close()
    return result