import DB as db
from tabulate import tabulate
import activate as activate

def admin_button_fun(message):
    #Кнопки
    # markupAdmin = types.InlineKeyboardMarkup()
    # buttonViewUsers = types.InlineKeyboardButton(text='Просмотреть пользователей UsersTab', callback_data='viewUsersTab')
    # buttonViewRas4et = types.InlineKeyboardButton(text='Просмотреть пользователей ras4etTab', callback_data='viewRas4etTab')
    # buttonSQL = types.InlineKeyboardButton(text='Свободный SQL запрос', callback_data='querySQL')
    # buttonCalcStart = types.InlineKeyboardButton(text='Включить калькулятор', callback_data='calcStart')
    # buttonActivate = types.InlineKeyboardButton(text='Активировать по промокоду', callback_data='activateByPromoCode')
    # markupAdmin.add(buttonViewUsers)
    # markupAdmin.add(buttonViewRas4et)
    # markupAdmin.add(buttonSQL)
    # markupAdmin.add(buttonCalcStart)
    # markupAdmin.add(buttonActivate)
    # bot.send_message(message.chat.id, 'Доступные функции', parse_mode='html', reply_markup=markupAdmin)
    #print(date.today())
    pass

def get_column_names_fun(tabName):
    connection=db.create_connection("ORPD.sqlite", 'Запрос админа')
    getColumnNames=connection.execute("select * from "+tabName+" limit 1")
    colName=[i[0] for i in getColumnNames.description]
    #print(colName)
    vivod='SELECT * FROM '+tabName+''
    viv=db.execute_read_query(connection, vivod)
    connection.close()
    result=tabulate(viv, headers=colName)
    return result

# Свободный SQL запрос, кроме чтения
def query_SQL_fun(message):
    query=f"{message.text}"
    mess='Подключение для выполнения свободного SQL-запроса'
    connection = db.create_connection("ORPD.sqlite", mess)
    print(query+'запрос')
    try:
        db.execute_query(connection,query,'Свободный запрос')
        #print(ch)
        #bot.send_message(message.chat.id, ch)
    except:
        return 'Ошибка в запросе'
    connection.close()






def activate_by_admin(message):
    message=str(message.text)
    #print(type(message))
    message=message.split('-')
    userID=message[0]
    #print(message)
    promoCode=activate.promo_code_check_fun(message[1])
    connection = db.create_connection("ORPD.sqlite", 'Подключение для активации подписки админом')
    quer=f"UPDATE users SET podpiska_do='{promoCode}' WHERE telegram_id={userID}; UPDATE ras4et SET prime4anie='active' WHERE telegram_id={userID}; UPDATE pipe SET prime4anie='active' WHERE telegram_id={userID};"
    db.execute_query(connection,quer,'Активация админом')
    connection.close()
    message_for_user = f'Вы получили подтверждение доната и активации, калькулятор будет работать без ограничений до <b>{promoCode}</b>.\n\nДля начала введите /start'
    message_for_admin = f'Запрос от пользователя {userID} на подписку на срок {promoCode} выполнено успешно'
    return [message_for_user, message_for_admin]
