import DB as db
import random
import calendar
from datetime import date, timedelta

def activate_fun(message,userID):
    promoCode=podpiska_do_fun(message)
    podpiskaDo=promo_code_check_fun(promoCode[0])
    connection = db.create_connection("ORPD.sqlite", 'Подключение для активации подписки юзера')
    print('podpiskaDo - ',podpiskaDo)
    checkUser=f"SELECT COUNT(telegram_id), podpiska_do FROM users WHERE telegram_id={userID} GROUP BY telegram_id"
    ch=db.execute_read_query(connection,checkUser,'Поиск юзера в базе')
    try:
        data=ch[0][1]
    except:
        data='1982-03-29'
    if ch!=[] and str(date.today())<data:
        # bot.send_message(userID, f'Информация о вашем запросе уже отправлена на проверку. Ожидайте подтверждения.\n\n/start', parse_mode='html')
        return [f'Информация о вашем запросе уже отправлена на проверку. Ожидайте подтверждения.\n\n/start',' ']
    else:
        ############# Проверка: не вставлять новую строку, а обновлять существующую строку
        if db.execute_read_query(connection, f'SELECT * FROM users WHERE telegram_id={userID}'):
            quer=f'UPDATE users SET podpiska_do="{promoCode[0]}" WHERE telegram_id={userID}'
        else:
            quer=f'INSERT INTO users (telegram_id, podpiska_do) VALUES ({userID}, "{promoCode[0]}")'
        db.execute_query(connection,quer,'Активация юзером')
        connection.close()

    return [f'Донат в размере {promoCode[1]} направляйте на <b>@ORPD_donate_bot</b>. \nПри проведении доната в комментарии укажите этот промокод -> \n\n"<b>{promoCode[0]}</b>"\n\nПосле доната вы получите подтверждение и калькулятор будет работать без ограничений до <b>{podpiskaDo}</b>.\nПока ждете подтверждения, введите /start для продолжения демо-режима.\n', f'Запрос от пользователя "{userID}" на подписку на срок {podpiskaDo} по промокоду "{promoCode[0]}"\n\n<b>{userID}-{promoCode[0]}</b>']
       
        # bot.send_message(userID, ,parse_mode='html')
    
        # bot.send_message(48691773, , parse_mode='html')



def promo_code_check_fun(promoCode):
    if len(promoCode)<21:
        return False
    i=0
    podpiskaDo=''
    while i<int(len(promoCode)):
        podpiskaDo+=promoCode[i]
        i+=3
    podpiskaDo=f'{podpiskaDo[:4]}-{podpiskaDo[4:6]}-{podpiskaDo[6:]}'
    return podpiskaDo
'''Пример использования
code=promo_code_check_fun(promoCode)
print(code)
'''

def promo_code_gen_fun(podpiskaDO):
    promoCode=''
    podpiskaDO=podpiskaDO.replace('-','')
    symbols='1234567890abcdefghijklmnopqrstuvwxyz1234567890!@#$%^&*№%:,.;1234567890 '
    i=0
    while i<int(len(podpiskaDO)):
        promoCode+=podpiskaDO[i]+symbols[random.randint(0,int(len(symbols))-1)]+symbols[random.randint(0,int(len(symbols))-1)]
        i+=1
    #print(promoCode)
    return promoCode

def podpiska_do_fun(before):
    today=date.today()
    if before=='month':
        daysPeriod = calendar.monthrange(today.year, today.month)[1]
        money='50 руб.'
    elif before=='half':
        daysPeriod = calendar.monthrange(today.year, today.month)[1]*6-2
        money='150 руб.'
    elif before=='year':
        daysPeriod = calendar.monthrange(today.year, today.month)[1]*12-6
        money='350 руб.'
    
    nextDate = today + timedelta(days=daysPeriod)
    #print(nextDate)
    p=[promo_code_gen_fun(str(nextDate)),money]
   
    return p