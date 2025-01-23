
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
    db.execute_query(connection, zapros, f'{param_name} внесение в БД')
    connection.close()
    # Конец работы с БД
    return True


def pipe_final_fun(message):
    connection = db.create_connection('ORPD.sqlite')
    q = f'SELECT * FROM pipe WHERE telegram_id={message.chat.id}'
    z ,= db.execute_read_query(connection, q)
    # (8, 48691773, 'Alexey N.', '1.0', '2.0', '3.0', '4.0', '5.0', 'Пар', '6.0', 'ТГ или НГ', None, 'no_active')
    _, user_id, user_name, rabD, rasD, rabT, rasT, nomD, sreda, skKorr, pipe_category, *_ = z
    rabD = float(rabD)
    rasD = float(rasD)
    rabT = float(rabT)
    rasT = float(rasT)
    nomD = float(nomD)
    skKorr = float(skKorr)
    if 'Класс 1' in pipe_category:
        category = 'I А (а)'
    elif 'Класс 3' in pipe_category and rabD>2.5 and (rabT>300 or rabT<-40):
        category = 'I А (б)'
    elif 'Класс 3' in pipe_category and rabD<-0.08:
        category = 'I А (б)'
    elif 'Класс 3' in pipe_category and -0.08<=rabD<=2.5 and -40<=rabT<=300:
        category = 'II А (б)'
    elif 'ГГ' in pipe_category and rabD>2.5 and (rabT>300 or rabT<-40):
        category = 'I Б (а)'
    elif 'ГГ' in pipe_category and rabD<-0.08:
        category = 'I Б (а)'
    elif 'ГГ' in pipe_category and -0.08<=rabD<=2.5 and -40<=rabT<=300:
        category = 'II Б (а)'
    elif 'ЛВЖ' in pipe_category and rabD>2.5 and (rabT>300 or rabT<-40):
        category = 'I Б (б)'
    elif 'ЛВЖ' in pipe_category and rabD<-0.08:
        category = 'I Б (б)'
    elif 'ЛВЖ' in pipe_category and 1.6<rabD<=2.5 and rabT<300:
        category = 'II Б (б)'
    else: category = 'V В'

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

Категория трубопровода - <b>{category}</b>.
'''
    connection.close()
    return result