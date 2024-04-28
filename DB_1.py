import sqlite3
from sqlite3 import Error
from tabulate import tabulate

createDefectsTable = """
CREATE TABLE IF NOT EXISTS defects (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  telegram_id INTEGER,
  defect TEXT
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

connection = create_connection("DEFECTS.sqlite",'Первое подключение к БД')

execute_query(connection,createDefectsTable, 'Проверка БД на существование таблицы Дефектов')

connection.close()