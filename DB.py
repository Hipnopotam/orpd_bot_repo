import sqlite3
from sqlite3 import Error
from tabulate import tabulate

createRas4etTable = """
CREATE TABLE IF NOT EXISTS ras4et (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  telegram_id INTEGER,
  name TEXT,
  rabD TEXT,
  rabT TEXT,
  sreda TEXT,
  tKip TEXT,
  obem TEXT,
  ntd TEXT,
  srTRTS TEXT,
  rtn TEXT,
  srok TEXT,
  sosType TEXT,
  pribavka TEXT,
  skKorr TEXT,
  prime4anie TEXT
);
"""

#Создание соединения к БД
def create_connection(path, mess="Подключение к БД SQLite - успешно"):
    connection = None
    try:
        connection = sqlite3.connect(path)
        print(mess)
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection

#Функция выполнения запросов к базе Insert, update, delete
def execute_query(connection, query, mess="Запрос к БД выполнен успешно"):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print(mess)
    except Error as e:
        mess=f"The error '{e}' occurred"
        print(mess)

#Функция чтения из БД
def execute_read_query(connection, query, mess='Чтение БД успешно'):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        print(mess)
        return result
    except Error as e:
        mess=f"the error '{e}' occurred"
        print(mess)

connection = create_connection("ORPD.sqlite",'Первое подключение к БД')
createUsersTable='''
CREATE TABLE IF NOT EXISTS users (
id INTEGER PRIMARY KEY AUTOINCREMENT,
telegram_id INTEGER,
podpiska_do TEXT
)
'''

# execute_query(connection,createRas4etTable, 'Проверка БД на существование таблицы расчета')
execute_query(connection,createUsersTable, 'Проверка БД на существование таблицы Юзеров')


# import DB as db

'''rabD - рабочее давление
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

deletePipeTable = 'drop table pipe'
connection = create_connection("ORPD.sqlite")
# execute_query(connection, deletePipeTable)
connection.close()

createPipeTable = """
CREATE TABLE IF NOT EXISTS pipe (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  telegram_id INTEGER,
  name TEXT,
  rabD TEXT,
  rasD TEXT
  rabT TEXT,
  rasT TEXT,
  dNom TEXT,
  sreda TEXT,
  pipe_category TEXT,
  revizia_pipe TEXT
  prime4anie TEXT
);
"""
connection = create_connection("ORPD.sqlite")
# execute_query(connection, createPipeTable)
connection.close()