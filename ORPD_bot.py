'''Hello everyone
сначала git stash
потом git pull
'''

import telebot
from telebot import types
import Super_secret as s
import DB as db
import functions as fun
import admin_fun as admin
import vessel_fun as vf
import pipe_fun as pf
import activate as activate
from time import sleep
from datetime import date

bot = telebot.TeleBot(s.token)


START = '''Основные функции калькулятора:

/start - начало (это сообщение)

/vessel - запуск калькулятора для расчета сосудов

/pipe - запуск калькулятора для расчета трубопроводов (в разработке)

/activate - активация полной версии калькулятора

/help - помощь
'''
'''
Запросы Active
1. Тип сосуда (сосуд/теплообменник)     - update_db_text_fun
2. Тип среды (газ/жидксоть/вода)        - update_db_text_fun
3. Группа среды по ТР ТС                - update_db_digit_fun
4. раб давление                         - update_db_digit_fun
5. раб температура                      - update_db_digit_fun
6.1 Темп кипения Газ = 0                - update_db_digit_fun
6.2 Темп кипения жидкости               - update_db_digit_fun
6.3 Темп кипения вода = 115             - update_db_digit_fun
7. объем                                - update_db_digit_fun
8. скорость коррозии                    - update_db_digit_fun
Результат - НТД, периодичность НВО ГИ спец

Запросы no_active
1. Тип сосуда (сосуд/теплообменник)     - update_db_text_fun
2. Тип среды (газ/жидксоть/вода)        - update_db_text_fun
3. раб давление                         - update_db_digit_fun
4. раб температура                      - update_db_digit_fun
5.1 Темп кипения Газ = 0                - update_db_digit_fun
5.2 Темп кипения жидкости               - update_db_digit_fun
5.3 Темп кипения вода = 115             - update_db_digit_fun
6. объем - update_db_digit_fun
Результат - НТД
'''
#Начало. При вводе /start
@bot.message_handler(commands=['start'])
def nachalo_fun(message):
    if message.chat.id==48691773:
        greeting = 'Здравствуй, мой разработчик <3'
        admin_button_fun(message)
        # fun.check_user_fun(message)
    else:
        # check_user_activate = fun.check_user_fun(message, 'ras4et')
        greeting = f"Здравствуйте, {message.from_user.first_name}." #\n\n{check_user_activate[1]}"
    bot.send_message(message.chat.id, greeting)
    bot.send_message(message.chat.id, START)

# При вводе /vessel
@bot.message_handler(commands=['vessel'])
def vessel_start(message):
    check_user_result = fun.check_user_fun(message, 'ras4et')
    # bot.send_message(message.chat.id, check_user_result[1])
    markup2 = types.InlineKeyboardMarkup()
    button_sosud = types.InlineKeyboardButton(text = 'Сосуд', callback_data='sosud')
    button_tepnik = types.InlineKeyboardButton(text = 'Теплообменник', callback_data='tepnik')
    markup2.add(button_sosud)
    markup2.add(button_tepnik)
    bot.send_message(message.chat.id, 'Выберете тип оборудования:', parse_mode='html', reply_markup=markup2)

def sos_type_fun(message):
    # vf.sos_type_fun(message) #text
    vf.update_db_text_fun(message, 'sosType')
    markup1 = types.InlineKeyboardMarkup()
    button_gas = types.InlineKeyboardButton(text = 'газ/пар', callback_data='gas')
    button_jidk = types.InlineKeyboardButton(text = 'жидкость', callback_data='jidk')
    button_water = types.InlineKeyboardButton(text = 'вода', callback_data='water')
    markup1.add(button_gas)
    markup1.add(button_jidk)
    markup1.add(button_water)
    bot.send_message(message.chat.id, 'Выберете тип среды:', reply_markup=markup1)

def sreda_jidk_fun(message):
    # vf.sreda_jidk_fun(message) # text
    vf.update_db_text_fun(message, 'sreda')
    mark = types.InlineKeyboardMarkup()
    if 'вода' not in message.text:
        button_1gr = types.InlineKeyboardButton(text = '1 группа', callback_data='gr1')
        mark.add(button_1gr)
        button_2gr = types.InlineKeyboardButton(text = '2 группа', callback_data='gr2')
        mark.add(button_2gr)
        bot.send_message(message.chat.id, 'Выберете группы среды по ТР ТС 032/2013', reply_markup=mark)
    elif 'вода' in message.text:
        # num4s = '2 группа'
        # num4 = bot.send_message(message.chat.id, num4s)
        sreda_TRTS_fun(bot.send_message(message.chat.id, '2 группа'))
    else:
        print('Ошибка 5')

def sreda_TRTS_fun(message):
    vf.update_db_text_fun(message, 'srTRTS')
    num1 = bot.send_message(message.chat.id, "Введите Рабочее давление, МПа:")
    bot.register_next_step_handler(num1, rabD_fun)

def rabD_fun(message):
    # rab_d = vf.rabD_fun(message) #digit
    rab_d=vf.update_db_digit_fun(message, 'rabD')
    if rab_d == None:
        num1 = bot.send_message(message.chat.id, "Введите Рабочее давление цифрами, МПа:")
        bot.register_next_step_handler(num1, rabD_fun)
    else:
        num2 = bot.send_message(message.chat.id, 'Введите Рабочую температуру, С:')
        bot.register_next_step_handler(num2 ,rabT_fun)

def rabT_fun(message):
    # rab_t = vf.rabT_fun(message)
    rab_t = vf.update_db_digit_fun(message, 'rabT')
    if rab_t == None:
        num1 = bot.send_message(message.chat.id, "Введите Рабочую температуру цифрами, С")
        bot.register_next_step_handler(num1, rabT_fun)
    else:
        sreda = vf.check_sreda_fun(message.chat.id)
        # print(sreda,' - sreda')
        if 'жидкость' in sreda:
            num2 = bot.send_message(message.chat.id, 'Введите температуру кипения, С:')
            bot.register_next_step_handler(num2 ,tKip_fun)
        elif 'вода' in sreda or 'газ' in sreda:
            num2 = bot.send_message(message.chat.id, 'Введите объем сосуда, м3:')
            bot.register_next_step_handler(num2 ,obem_fun)
        else:
            print('ошибка 4')
        # СДЕЛАТЬ ТУТ ВНЕСЕНИЕ Т КИП ДЛЯ ГАЗА И ВОДЫ В БД

def tKip_fun(message):
    # t_kip = vf.tKip_fun(message)
    t_kip = vf.update_db_digit_fun(message, 'tKip')
    if t_kip == None:
        num1 = bot.send_message(message.chat.id, "Введите температуру кипения цифрами, С")
        bot.register_next_step_handler(num1, tKip_fun)
    else:
        num2 = bot.send_message(message.chat.id, 'Введите объем сосуда, м3:')
        bot.register_next_step_handler(num2 ,obem_fun)

def obem_fun(message):
    # obem = vf.obem_fun(message)
    obem = vf.update_db_digit_fun(message, 'obem')
    if obem == None:
        num1 = bot.send_message(message.chat.id, "Введите объем цифрами, С")
        bot.register_next_step_handler(num1, obem_fun)
    else:
        num2 = bot.send_message(message.chat.id, 'Введите скорость коррозии, мм/год:')
        bot.register_next_step_handler(num2, sk_korr_fun)

def sk_korr_fun(message):
    sk_korr = vf.update_db_digit_fun(message, 'skKorr')
    if sk_korr == None:
        num1 = bot.send_message(message.chat.id, 'Введите скорость коррозии цифрами, мм/год')
        bot.register_next_step_handler(num1, sk_korr_fun)
    else:
        result_fun(message)

def result_fun(message):
    result=vf.result_fun(message)
    bot.send_message(message.chat.id, result)
    # print(result, '- result')
    rtn = vf.rtn_fun(message)
    bot.send_message(message.chat.id, rtn)
    revizia = str(vf.revizia_fun(message)) + '\n\nДля продолжения введите /vessel.\nИли введите /start'
    bot.send_message(message.chat.id, revizia)

####################################################################
#########^^^^^^^^^^ Начало расчета трубопроводов ^^^^^^^^^^#########


#при вводе activate
@bot.message_handler(commands=['pipe'])
def pipe_start(message):
    fun.check_user_fun(message, 'pipe')
    num1 = bot.send_message(message.chat.id, "Введите рабочее давление, МПа")
    bot.register_next_step_handler(num1, pipe_rabD_fun)

def pipe_rabD_fun(message):
    rabD = pf.pipe_digit_fun(message, 'rabD')
    if rabD == None:
        mess = bot.send_message(message.chat.id, 'Введите рабочее давление цифрами, МПа:')
        bot.register_next_step_handler(mess, pipe_rabD_fun)
    else:
        mess = bot.send_message(message.chat.id, 'Введите расчетное давление, МПа:')
        bot.register_next_step_handler(mess, pipe_rasD_fun)

def pipe_rasD_fun(message):
    rasD = pf.pipe_digit_fun(message, 'rasD')
    if rasD == None:
        mess = bot.send_message(message.chat.id, 'Введите расчетное давление цифрами, МПа:')
        bot.register_next_step_handler(mess, pipe_rasD_fun)
    else:
        mess = bot.send_message(message.chat.id, 'Введите рабочую температуру, C:')
        bot.register_next_step_handler(mess, pipe_rabT_fun)

def pipe_rabT_fun(message):
    rabT = pf.pipe_digit_fun(message, 'rabT')
    if rabT == None:
        mess = bot.send_message(message.chat.id, 'Введите рабочую температуру цифрами, МПа:')
        bot.register_next_step_handler(mess, pipe_rasD_fun)
    else:
        mess = bot.send_message(message.chat.id, 'Введите расчетную температуру, C: ')
        bot.register_next_step_handler(mess, pipe_rasT_fun)

def pipe_rasT_fun(message):
    rasT = pf.pipe_digit_fun(message, 'rasT')
    if rasT == None:
        mess = bot.send_message(message.chat.id, 'Введите расчетную температуру цифрами, МПа')
        bot.register_next_step_handler(mess, pipe_rasT_fun)
    else:
        mess = bot.send_message(message.chat.id, 'Введите номинальный диаметр, мм:')
        bot.register_next_step_handler(mess, pipe_nomD_fun)
    
def pipe_nomD_fun(message):
    nomD = pf.pipe_digit_fun(message, 'nomD')
    if nomD == None:
        mess = bot.send_message(message.chat.id, 'Введите номинальный диаметр цифрами, мм')
        bot.register_next_step_handler(mess, pipe_nomD_fun)
    else:
        mess = bot.send_message(message.chat.id, 'Введите скорость коррозии, мм/год')
        bot.register_next_step_handler(mess, pipe_skKorr_fun)

def pipe_skKorr_fun(message):
    skKorr = pf.pipe_digit_fun(message, 'skKorr')
    if skKorr == None:
        mess = bot.send_message(message.chat.id, 'Введите скорость коррозии цифрами, мм/год')
        bot.register_next_step_handler(mess, pipe_skKorr_fun)
    else:
        markup5 = types.InlineKeyboardMarkup()
        pipe_button_gas = types.InlineKeyboardButton(text = 'Газ', callback_data='Gas')
        pipe_button_steam = types.InlineKeyboardButton(text = 'Пар', callback_data='steam')
        pipe_button_liquid = types.InlineKeyboardButton(text = 'жидкость', callback_data='liquid')
        markup5.add(pipe_button_gas)
        markup5.add(pipe_button_steam)
        markup5.add(pipe_button_liquid)
        bot.send_message(message.chat.id, 'Введите тип среды:', parse_mode='html', reply_markup=markup5)

def pipe_sreda_fun(message):
    pf.pipe_text_fun(message, 'sreda')
    markup6 = types.InlineKeyboardMarkup()
    pipe_button_toxic12 = types.InlineKeyboardButton(text = 'Токсичная: Класс 1, Класс 2', callback_data='toxic_12')
    pipe_button_toxic3 = types.InlineKeyboardButton(text = 'Токсичная: Класс 3', callback_data='toxic_3')
    pipe_button_gg_sug = types.InlineKeyboardButton(text = 'Взрывопожароопасные: ГГ или СУГ', callback_data='gg_sug')
    pipe_button_lvj = types.InlineKeyboardButton(text = 'Взрывопожароопасные: ЛВЖ, ГЖ', callback_data='lvj')
    pipe_button_gj = types.InlineKeyboardButton(text = 'Взрывопожароопасные: ГЖ', callback_data='gj')
    pipe_button_not_fire = types.InlineKeyboardButton(text = 'ТГ или НГ', callback_data='not_fire')
    markup6.add(pipe_button_toxic12)
    markup6.add(pipe_button_toxic3)
    markup6.add(pipe_button_gg_sug)
    markup6.add(pipe_button_lvj)
    markup6.add(pipe_button_gj)
    markup6.add(pipe_button_not_fire)
    bot.send_message(message.chat.id, 'Введите группу среды:', parse_mode='html', reply_markup=markup6)

def pipe_category_fun(message):
    pf.pipe_text_fun(message, 'pipe_category')
    pipe_final_fun(message)
    
   

def pipe_final_fun(message):
    result = pf.pipe_final_fun(message)
    bot.send_message(message.chat.id, f'Результат: \n\n {result}', parse_mode='html')

#########^^^^^^^^^^ Конец расчета трубопроводов ^^^^^^^^^^#########

#######################################################

##############          АДМИНКА          ##############

#######################################################

#при вводе activate
@bot.message_handler(commands=['activate'])
def test_request_fun(message):
    connection = db.create_connection("ORPD.sqlite", 'Подключение для активации подписки юзера')
    checkUser=f"SELECT COUNT(telegram_id), podpiska_do FROM users WHERE telegram_id={message.chat.id} GROUP BY telegram_id"
    ch=db.execute_read_query(connection,checkUser,'Поиск юзера в базе')
    try:
        data=ch[0][1]
    except:
        data='1982-03-29'
    if ch!=[] and str(date.today())<data:
        bot.send_message(message.chat.id, f'Ваша подписка действует до {data}\n\nДля продолжения введите /start')
        return
    
    markup2 = types.InlineKeyboardMarkup()
    button_month = types.InlineKeyboardButton(text = '1 месяц', callback_data='month')
    button_half = types.InlineKeyboardButton(text = '6 месяцев', callback_data='half')
    button_year = types.InlineKeyboardButton(text = 'Год', callback_data='year')
    markup2.add(button_month)
    markup2.add(button_half)
    markup2.add(button_year)
    bot.send_message(message.chat.id, 'Выберете срок подписки:', parse_mode='html', reply_markup=markup2)


def admin_button_fun(message):
    #Кнопки
    markupAdmin = types.InlineKeyboardMarkup()
    buttonViewUsers = types.InlineKeyboardButton(text='Просмотреть пользователей UsersTab', callback_data='viewUsersTab')
    buttonViewRas4et = types.InlineKeyboardButton(text='Просмотреть пользователей Vessel', callback_data='viewRas4etTab')
    buttonViewPipe = types.InlineKeyboardButton(text='Просмотреть пользователей Pipe', callback_data='viewPipeTab')
    buttonSQL = types.InlineKeyboardButton(text='Свободный SQL запрос', callback_data='querySQL')
    # buttonCalcStart = types.InlineKeyboardButton(text='Включить калькулятор', callback_data='calcStart')
    buttonActivate = types.InlineKeyboardButton(text='Активировать по промокоду', callback_data='activateByPromoCode')
    markupAdmin.add(buttonViewUsers)
    markupAdmin.add(buttonViewRas4et)
    markupAdmin.add(buttonViewPipe)
    markupAdmin.add(buttonSQL)
    # markupAdmin.add(buttonCalcStart)
    markupAdmin.add(buttonActivate)
    bot.send_message(message.chat.id, 'Доступные функции', parse_mode='html', reply_markup=markupAdmin)
    #print(date.today())


def activate_fun(message, userID):
    activ=activate.activate_fun(message, userID)
    # print(activ, 'yeah')
    message_for_user = activ[0]
    message_for_admin = activ[1]
    bot.send_message(userID, message_for_user, parse_mode='HTML')
    bot.send_message(48691773, message_for_admin, parse_mode='HTML')

def activate_by_admin(message):
    activ_admin = admin.activate_by_admin(message)
    if activ_admin== None:
        bot.send_message(48691773, 'Ошибка активации админом')
    else:
        message_for_user, message_for_admin = activ_admin
        bot.send_message(message.chat.id, message_for_user, parse_mode='HTML')
        bot.send_message(48691773, message_for_admin)



###################################### Все кнопки #####################################

@bot.callback_query_handler(func=lambda call:True)
def response(function_call):
    if function_call.message:
        if function_call.data == "gas":
            num4s='газ'
            num4=bot.send_message(function_call.message.chat.id, num4s)
            sreda_jidk_fun(num4)
        elif function_call.data == "water":
            num4s='вода'
            num4=bot.send_message(function_call.message.chat.id, num4s)
            sreda_jidk_fun(num4)
        elif function_call.data == "jidk":
            num4s='жидкость'
            num4=bot.send_message(function_call.message.chat.id, num4s)
            sreda_jidk_fun(num4)
        elif function_call.data == "gr1":
            num4s='1 группа'
            num4=bot.send_message(function_call.message.chat.id, num4s)
            sreda_TRTS_fun(num4)
        elif function_call.data == "gr2":
            num4s='2 группа'
            num4=bot.send_message(function_call.message.chat.id, num4s)
            sreda_TRTS_fun(num4)
        elif function_call.data == 'sosud':
            num4s='Сосуд'
            num4=bot.send_message(function_call.message.chat.id, num4s)
            sos_type_fun(num4)
        elif function_call.data == 'tepnik':
            num4s='Теплообменник'
            num4=bot.send_message(function_call.message.chat.id, num4s)
            sos_type_fun(num4)
        elif function_call.data == 'viewUsersTab':
            mess=admin.get_column_names_fun('users')
            bot.send_message(function_call.message.chat.id, mess)
        elif function_call.data == 'viewRas4etTab':
            mess=admin.get_column_names_fun('ras4et')
            bot.send_message(function_call.message.chat.id, mess)
        elif function_call.data == 'viewPipeTab':
            mess=admin.get_column_names_fun('pipe')
            bot.send_message(function_call.message.chat.id, mess)
        # elif function_call.data=='calcStart':
        #     num1 = bot.send_message(function_call.message.chat.id, "Введите Рабочее давление, МПа:")
        #     bot.register_next_step_handler(num1, rabD_fun)
        elif function_call.data == 'querySQL':
            quer=bot.send_message(function_call.message.chat.id,'Введите SQL запрос')
            bot.register_next_step_handler(quer, admin.query_SQL_fun)
        ########################################
        ############# Кнопки pipe ##############
        elif function_call.data == 'Gas':
            mess = bot.send_message(function_call.message.chat.id, 'Газ')
            pipe_sreda_fun(mess)
        elif function_call.data == 'steam':
            mess = bot.send_message(function_call.message.chat.id, 'Пар')
            pipe_sreda_fun(mess)
        elif function_call.data == 'liquid':
            mess = bot.send_message(function_call.message.chat.id, 'Жидкость')
            pipe_sreda_fun(mess)
        elif function_call.data == 'toxic_12':
            mess = bot.send_message(function_call.message.chat.id, 'Токсичные: Класс 1, Класс 2')
            pipe_category_fun(mess)
        elif function_call.data == 'toxic_3':
            mess = bot.send_message(function_call.message.chat.id, 'Токсичные: Класс 3')
            pipe_category_fun(mess)
        elif function_call.data == 'gg_sug':
            mess = bot.send_message(function_call.message.chat.id, 'Взрывопожароопасные: ГГ или СУГ')
            pipe_category_fun(mess)
        elif function_call.data == 'lvj':
            mess = bot.send_message(function_call.message.chat.id, 'Взрывопожароопасные: ЛВЖ')
            pipe_category_fun(mess)
        elif function_call.data == 'gj':
            mess = bot.send_message(function_call.message.chat.id, 'Взрывопожароопасные: ГЖ')
            pipe_category_fun(mess)
        elif function_call.data == 'not_fire':
            mess = bot.send_message(function_call.message.chat.id, 'ТГ или НГ')
            pipe_category_fun(mess)
        ########################################
        ############ КНОПКИ ПОДПИСКИ ###########
        elif function_call.data=='month':
            mess='month'
            activate_fun(mess, function_call.message.chat.id)
        elif function_call.data=='half':
            mess='half'
            activate_fun(mess, function_call.message.chat.id)
        elif function_call.data=='year':
            mess='year'
            activate_fun(mess, function_call.message.chat.id)
        elif function_call.data=='activateByPromoCode':
            quer=bot.send_message(function_call.message.chat.id,'Введите промокод от Юзера (UserID-Promocode)')
            bot.register_next_step_handler(quer, activate_by_admin)   
        #########################################
        ############ КОНЕЦ КНОПОК ПОДПИСКИ ######
        else:
            bot.send_message(function_call.message.chat.id, 'ошибка 2')





# При вводе /help
@bot.message_handler(commands=['help'])
def handle_text1(message):
    mess='''
Здравствуйте.
Если вы зашли сюда, то скорее всего вы либо инженер, либо <i>сочуствующий</i>.

Я решил реализовать этот проект, просто потому что мне интересно этим заниматься.

Вы просто вводите все минимально необходимые сведения по вашему оборудованию и в конце получаете ответ.
Конечно, я рекомендую всегда и все перепроверять.
Но однако же, надеюсь, что он вам поможет.

Для начала работы калькулятора введите /start
Для получения полного доступа и активации подписки введите /activate

По вопросам работы калькулятора и сотрудничеству пишите на <b>@hipnopotam</b>


Список используемой литературы:
1. Федеральные нормы и правила в области промышленной безопасности "Правила промышленной безопасности при использовании оборудования, работающего под избыточным давлением" Приказ от 15 декабря 2020 года № 536 - далее <b><a href="https://yandex.ru/search/?text=фнп+536&lr=35&src=suggest_B">ФНП</a></b>.

2. Технический регламент Таможенного союза "О безопасности оборудования, работающего под избыточным давлением" (ТР ТС 032/2013) - далее <b><a href="https://yandex.ru/search/?text=тр+тс+032&lr=35&src=suggest_B">ТР ТС</a></b>.

3. Руководящие указания по эксплуатации и ремонту сосудов и аппаратов, работающих под давлением ниже 0,07 МПа (0,7 кгс/кв. см) и вакуумом - далее <b><a href="https://yandex.ru/search/?text=руа-93&lr=35">РУА-93</a></b>.

4. Инструкция по техническому надзору и эксплуатации сосудов, работающих под давлением, на которые не распространяются Правила Госгортехнадзора - далее <b><a href="https://yandex.ru/search/?text=итнэ-93&lr=35">ИТНЭ-93</a></b>.
'''
    bot.send_message(message.chat.id, mess, parse_mode='html')









# Это должно быть в самом конце
bot.polling(none_stop=True, interval=0)

# while True:
#     try:
#         bot.polling(none_stop=True)
#     except Exception as _ex:
#         print(_ex)
#         sleep(15)
