import DB as db
import time
from datetime import date

#Функция замены запятой на точку
def zapyataya(t):
    if t.find(',')!=-1:
        t=str(t.replace(',','.'))
        return t
    else:
        t=str(t)
        return t

#Функция проверки на число
def check_digit(param):
    p=zapyataya(param)
    try:
        p=int(p)
        t=1
    except:
        t=0
    try:
        p=float(p)
        tt=1
    except:
        tt=0
    if t+tt>0:
        return True
    else:
        return False
    

def check_user_fun(message):
    check_user_result = ['',0]
    mess='Подключение для проверки на сущ юзера'
    connection = db.create_connection("ORPD.sqlite", mess)
    checkUser=f"SELECT COUNT(telegram_id), podpiska_do FROM users WHERE telegram_id={message.from_user.id} GROUP BY telegram_id"
    ch=db.execute_read_query(connection,checkUser,'Поиск юзера в базе')

    if ch and ch[0][1].find('-')!=-1:
        a=ch[0][0]
        podpiska_do=ch[0][1]
        print(a,podpiska_do)
    else:
        a=0
        podpiska_do=''
        print('нету юзера')

    if ch!=[] and str(date.today())<podpiska_do and len(podpiska_do)==10:
        cleaner=f'DELETE FROM ras4et WHERE telegram_id={message.from_user.id}'
        db.execute_query(connection,cleaner,'Cleaner')
        
        newUserQuery=f"INSERT INTO ras4et ('telegram_id','name', 'prime4anie') VALUES ({message.from_user.id}, '{message.from_user.first_name} {message.from_user.last_name}', 'active')"
        db.execute_query(connection,newUserQuery)
        # handle_text(message)
        check_user_result = ['Ваша подписка активна', 1]
        
    else:
        cleaner=f'DELETE FROM ras4et WHERE telegram_id={message.from_user.id}'
        db.execute_query(connection,cleaner,'Cleaner')

        if str(date.today())>podpiska_do and podpiska_do!='':
            data=podpiska_do.split('-')
            day=data[2]
            month=data[1]
            year=data[0]
            tex='У вас закончилась подписка '+day+'.'+month+'.'+year+'. '
            print('У Юзера закончилась подписка')
        else:
            tex='У вас не оформлена подписка. '
            print('Юзер в БД отсутствует')
        tex=tex+"Калькулятор пока работает в тестовом режиме. \nСкоро заработает в полную силу, но только для подписчиков.\nА пока предлагаю ознакомиться с демо-версией\n\nДля подписки введите /activate"
    
        newUserQuery=f"INSERT INTO ras4et ('telegram_id','name', 'prime4anie') VALUES ({message.from_user.id}, '{message.from_user.first_name} {message.from_user.last_name}', 'no_active')"
        db.execute_query(connection,newUserQuery)
        check_user_result = [0, tex]
        # handle_text(message)
    connection.close()
    return check_user_result