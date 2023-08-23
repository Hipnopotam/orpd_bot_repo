import functions as fun
import DB as db
from tabulate import tabulate


def rabD_fun(message, warning=' '):
    # print(message.chat.id)
    rabD= str(message.text)
    if fun.check_digit(rabD)!=False:
        p=fun.zapyataya(rabD)
        rabD=float(p)
        #работа с БД
        connection = db.create_connection("ORPD.sqlite", '1')
        zapros=f'UPDATE ras4et SET rabD={rabD} WHERE telegram_id={message.chat.id}'
        db.execute_query(connection, zapros, 'рабочее давление внесение в БД')
        connection.close()
        #конец работы с БД
        return warning
    else:
        warning = 'Введите рабочее давление цифрами, МПа:'
        return None
    
def rabT_fun(message, warning=' '):
    rabT = str(message.text)
    if fun.check_digit(rabT)!=False:
        p=fun.zapyataya(rabT)
        rabT=float(p)
        #работа с БД
        connection = db.create_connection("ORPD.sqlite",'2')
        zapros=f'UPDATE ras4et SET rabT={rabT} WHERE telegram_id={message.chat.id}'
        db.execute_query(connection, zapros, 'рабочая температура внесение в БД')
        connection.close()
        #конец работы с БД
        return warning
    else:
        warning = 'Введите рабочую температуру цифрами, C'
        return None
    
def obem_fun(message, warning=' '):
    t=message.text
    if t=='газ':
        tKip=float(0)
        sreda=t
        warning = 'Введите объем сосуда, м3:'
    elif t=='вода':
        tKip=115
        sreda=t
        warning = 'Введите объем сосуда, м3:'
    else:
        tKip=str(t)
        sreda='жидкость'
        if fun.check_digit(tKip)!=False:
            tKip=float(fun.zapyataya(tKip))
            warning = 'Введите объем сосуда, м3:'
        else:
            return None
    #работа с БД
    connection = db.create_connection("ORPD.sqlite",'3')
    zapros1=f"UPDATE ras4et SET sreda='{sreda}', tKip='{tKip}' WHERE telegram_id={message.chat.id}"
    db.execute_query(connection, zapros1, 'среда внесение в БД num4')
    connection.close()
    return warning
    #конец работы с БД

def sreda_jidk_fun(message):
    #работа с БД
    connection = db.create_connection("ORPD.sqlite", '1')
    zapros1=f"UPDATE ras4et SET sreda='жидкость' WHERE telegram_id={message.chat.id}"
    db.execute_query(connection, zapros1, 'среда внесение в БД num2')
    connection.close()
    #конец работы с БД


def ntd_fun(message):
    obem = str(message.text)
    if fun.check_digit(obem)==False:
        return None
    else:
        obem=float(fun.zapyataya(obem))
        #работа с БД
        connection = db.create_connection("ORPD.sqlite",'4')
        zapros=f'UPDATE ras4et SET obem={obem} WHERE telegram_id={message.chat.id}'
        db.execute_query(connection, zapros, 'объем внесение в БД')

        #Запрос из БД-таблицы ras4et - рабочего давления, среда, темп кипения
        zapros1=f'SELECT rabD, sreda, tKip, rabT, prime4anie FROM ras4et WHERE telegram_id={message.chat.id}'
        zap=db.execute_read_query(connection,zapros1,'Запрос')
        header=['рабД','среда','Ткипен', 'РабТ', 'подписка']
        print(tabulate(zap, headers=header, tablefmt='grid'))
        rabD=float(zap[0][0])
        sreda=zap[0][1]
        tKip=float(zap[0][2])
        rabT=float(zap[0][3])
        podpiska=zap[0][4]

        resultNTD=ntd_fun_result(rabD,obem,rabT,tKip,sreda)
        ntdMess=resultNTD[1]
        # print('ntdMess - ',ntdMess)
        ntd=resultNTD[0]

        t=f'Параметры сосуда:\nРабочее давление - {rabD} МПа, \nРабочая температура - {rabT} С,\nОбъем сосуда - {obem} м3, \nСреда - {sreda}\nПроизведение давления на вместимость - {str(round(rabD*obem,5))}.'
        result =  t+'\n\n'+ntdMess

        zapros=f"UPDATE ras4et SET ntd='{ntd}' WHERE telegram_id={message.chat.id}"
        db.execute_query(connection, zapros, 'НТД внесение в БД')
        connection.close()
        #конец работы с БД

        if podpiska=='no_active':
            result += '\n\nНа этом обзор демо версии окончен. В полной версии вы можете рассчитать периодичность НВО и ГИ, необходимость постановки на учет в РТН.\n\n Для просмотра главного меню введите /start\n\nДля расчета сосудов введите /vessel\n\nДля расчета трубопроводов введите /pipe\n\nДля активации введите /activate'
            return result
        

        if ntd!='ФНП' and podpiska!='no_active': #Дописать проверку на активную подписку
            result_fnp = fnp_fun(ntd,0,rabT,rabD,obem)
            result_ntd = ntd_fun_result(rabD,obem,rabT,tKip,sreda)
            # r=bot.send_message(message.chat.id, result[1], parse_mode='html')
            #работа с БД
            connection = db.create_connection("ORPD.sqlite",'5')
            zapros=f"UPDATE ras4et SET rtn='0' WHERE telegram_id={message.chat.id}"
            db.execute_query(connection, zapros, 'РТН внесение в БД')
            connection.close()
            #конец работы с БД

            result += f"\n\n{result_fnp}"
            # print(result, ' -  result')
            return result

        elif ntd=='ФНП' and podpiska!='no_active':
            rtnMess='\n\nДля проверки необходимости постановки на учет в РТН введите группу среды по ТР ТС 032:'
            
        result += rtnMess
        return result


def ntd_fun_result(rabD,obem,rabT,tKip,sreda):
    if rabD>0.07 and obem<=0.025 and obem*rabD<=0.02:
        ntdMess='На сосуд распространяется ИТНЭ-93. \nСогласно пункта 5 ж) ФНП ОРПД - сосуд не подпадает под ФНП.'
        ntd='ИТНЭ'
    elif rabD>0.07 and rabT>tKip and (sreda=='Жидкость' or sreda=='жидкость'):
        ntdMess='На сосуд распространяется ФНП ОРПД - ст.2 в).'
        ntd='ФНП'
    elif rabD>0.07 and (sreda=='газ' or sreda=='Газ'):
        ntdMess='На сосуд распространяется ФНП ОРПД - ст.2 а).'
        ntd='ФНП'
    elif obem*rabD>0.02 and rabD>0.07 and obem<=0.025:
        ntdMess='На сосуд распространяется ФНП ОРПД - ст.5 ж).'
        ntd='ФНП'
    elif rabD>0.07 and (sreda=='вода' or sreda=='Вода') and rabT>115:
        ntdMess='На сосуд распространяется ФНП ОРПД - ст.2 б).'
        ntd='ФНП'
    elif rabD<=0.07:
        ntdMess='На сосуд распространяется РУА-93.'
        ntd='РУА'
    else:
        ntdMess='На сосуд распространяется ИТНЭ-93.'
        ntd='ИТНЭ'
    result=[ntd,ntdMess]
    return result




def rtn_fun(message):
    connection = db.create_connection("ORPD.sqlite", '6')
    zapros=f'SELECT rabT, obem, ntd, rabD, prime4anie FROM ras4et WHERE telegram_id={message.chat.id}'
    zap=db.execute_read_query(connection,zapros,'Запрос')
    header=['РабТ', 'объем', 'НТД', 'рабД', 'подписку']
    print(tabulate(zap, headers=header,tablefmt='grid'))
    rabT=float(zap[0][0])
    obem=float(zap[0][1])
    ntd=zap[0][2]
    rabD=float(zap[0][3])
    srTRTS=str(message.text)
    podpiska=str(zap[0][4])

    result=fnp_fun(ntd,srTRTS,rabT,rabD,obem)
    rtnMess=result
    if 'не надо'in rtnMess:
        rtn=0
    else:
        rtn=1
    #работа с БД
    zapros=f"UPDATE ras4et SET rtn='{rtn}', srTRTS='{srTRTS}' WHERE telegram_id={message.chat.id}"
    db.execute_query(connection, zapros, 'РТН внесение в БД')
    connection.close()
    #конец работы с БД
    return rtnMess


def sos_type_fun(message):
    sosType=str(message.text)
    #работа с БД
    connection = db.create_connection("ORPD.sqlite", '8')
    zapros=f"UPDATE ras4et SET sosType='{sosType}' WHERE telegram_id={message.chat.id}"
    db.execute_query(connection, zapros, 'Тип сосуда внесение в БД')
    connection.close()
    #конец работы с БД
    result = 'Введите прибавку на коррозию, мм'
    return result



def fnp_fun(ntd,srTRTS,rabT,rabD,obem):
    if ntd=='ФНП':
        if srTRTS=='1 группа' and (rabT>200 or rabD*obem>0.05):
            rtn=1
            rtnMess='Сосуд необходимо ставить на учет в РТН.'
        elif srTRTS=='2 группа' and (rabT>200 or rabD*obem>1):
            rtn=1
            rtnMess='Сосуд необходимо ставить на учет в РТН.'
        else:
            rtn=0
            rtnMess='Сосуд на учет в РТН ставить не надо. Статья 223 а).'
    else:
        rtn=0
        rtnMess='Сосуд на учет в РТН ставить не надо.'
    rtnMess=rtnMess+'\n\n\nДля расчета периодичности ревизии введите назначенный срок эксплуатации, лет'
    result=rtnMess
    return result

def srok_fun(message, warning='ok'):
    srok = str(message.text)
    print(srok)
    if fun.check_digit(srok) == False:
        return None
    else:
        srok = float(fun.zapyataya(srok))
        #работа с БД
        connection = db.create_connection("ORPD.sqlite", '7')
        zapros = f"UPDATE ras4et SET srok='{srok}' WHERE telegram_id={message.chat.id}"
        db.execute_query(connection, zapros, 'Срок внесение в БД')
        connection.close()
        #конец работы с БД
        return warning
    

def pribavka_fun(message):
    connection = db.create_connection("ORPD.sqlite", '9')
    zapros2=f'SELECT ntd, rtn, sosType, srok FROM ras4et WHERE telegram_id={message.chat.id}'
    zap=db.execute_read_query(connection,zapros2,'Запрос')
    header=['НТД', 'РТН', 'тип сосуда', 'срок']
    
    print(tabulate(zap, headers=header, tablefmt='grid'))
    ntd=zap[0][0]
    rtn=int(zap[0][1])
    sosType=zap[0][2]
    srok=float(zap[0][3])
    pribavka=str(message.text)
    if fun.check_digit(pribavka)==False:
        return None
    else:
        pribavka=float(fun.zapyataya(pribavka))
        skKorr=round(pribavka/srok,4)

        result = f'Расчетная скорость коррозии: <b>{skKorr}</b> мм/год'
        #работа с БД
        zapros=f"UPDATE ras4et SET pribavka='{pribavka}', skKorr='{skKorr}' WHERE telegram_id={message.chat.id}"
        db.execute_query(connection, zapros, 'Прибавка и ск. корр. внесение в БД')
        
        #вывод таблицы ras4et
        getColumnNames=connection.execute("select * from ras4et limit 1")
        colName=[i[0] for i in getColumnNames.description]

        vivod=f'SELECT * FROM ras4et WHERE telegram_id={message.chat.id}'
        viv=db.execute_read_query(connection, vivod)
        print(tabulate(viv, headers=colName, tablefmt='grid'))
        
        #конец работы с БД
        
        resultRevizia=revizia_fun(ntd,rtn,skKorr,sosType)

        result += '\n\n'+resultRevizia
    connection.close()
    result += '\n\n\n' + 'Для просмотра главного меню введите /start\n\nДля расчета сосудов введите /vessel\n\nдля расчета трубопроводов введите /pipe'
    return result




    #       НВО                         ГИ                          НВО-отв                     НВО-спец                     ГИ
#       ФНП-да, учет-нет            ФНП-да, учет-нет            ФНП-да, учет-да
nvoFNP=[['6 лет','2 года','1 год'], ['12 лет','8 лет','8 лет'], ['6 лет','2 года','1 год'], ['6 лет','4 года','4 года'], ['12 лет','8 лет','8 лет']]

#периодичность ревизии по РУА-93, ИТНЭ"-93
#Тип сосуда Сосуд                                           Теплообменник
#           НВО         ГИ          НВО         ГИ          НВО         ГИ          НВО         ГИ
#гр. сосуда 1           1           2           2           1           1           2           2
nvoRUA01=   ['6 лет',   '12 лет',   '12 лет',   '12 лет',   '12 лет',   '12 лет',   '12 лет',    '12 лет']
nvoRUA0103= ['2 года',  '8 лет',    '4 года',   '8 лет',    '8 лет',    '8 лет',    '8 лет',    '8 лет']
nvoRUA03=   ['1 год',   '8 лет',    '2 года',   '8 лет',    '1 год',    '8 лет',    '2 года',   '8 лет']


def revizia_fun(ntd,rtn,skKorr,sosType):
    # ФНП
    if ntd=='ФНП' and rtn==0 and skKorr<=0.1 and sosType=='Сосуд':
        resultRevizia= f'Периодичность проведения НВО:\nОтветственным - раз в {nvoFNP[0][0]}\n\nПериодичность проведения ГИ:\nРаз в - {nvoFNP[1][0]}'
    elif ntd=='ФНП' and rtn==0 and 0.1<skKorr<=0.3 and sosType=='Сосуд':
        resultRevizia=f'Периодичность проведения НВО:\nОтветственным - раз в {nvoFNP[0][1]}\n\nПериодичность проведения ГИ:\nРаз в - {nvoFNP[1][1]}'
    elif ntd=='ФНП' and rtn==0 and skKorr>0.3 and sosType=='Сосуд':
        resultRevizia=f'Периодичность проведения НВО:\nОтветственным - раз в {nvoFNP[0][2]}\n\nПериодичность проведения ГИ:\nРаз в - {nvoFNP[1][2]}'
    elif rtn==1 and skKorr<=0.1 and sosType=='Сосуд':
        resultRevizia=f'Периодичность проведения НВО:\nОтветственным - раз в {nvoFNP[2][0]}\nСпец. организацией - раз в {nvoFNP[3][0]}\n\nПериодичность проведения ГИ:\nРаз в - {nvoFNP[4][0]}'
    elif rtn==1 and 0.1<skKorr<=0.3 and sosType=='Сосуд':
        resultRevizia=f'Периодичность проведения НВО:\nОтветственным - раз в {nvoFNP[2][1]}\nСпец. организацией - раз в {nvoFNP[3][1]}\n\nПериодичность проведения ГИ:\nРаз в - {nvoFNP[4][1]}'
    elif rtn==1 and skKorr>0.3 and sosType=='Сосуд':
        resultRevizia=f'Периодичность проведения НВО:\nОтветственным - раз в {nvoFNP[2][2]}\nСпец. организацией - раз в {nvoFNP[3][2]}\n\nПериодичность проведения ГИ:\nРаз в {nvoFNP[4][2]}'
    elif rtn==1 and skKorr<=0.1 and sosType=='Теплообменник':
        resultRevizia='Периодичность проведения НВО:\nОтветственным - после каждой выемки трубной системы.\nСпец. организацией - раз в 12 лет\n\nПериодичность проведения ГИ:\nРаз в 12 лет'
    elif rtn==1 and 0.1<skKorr<=0.3 and sosType=='Теплообменник':
        resultRevizia='Периодичность проведения НВО:\nОтветственным - после каждой выемки трубной системы.\nСпец. организацией - раз в 8 лет\n\nПериодичность проведения ГИ:\nРаз в 8 лет'
    elif rtn==1 and skKorr>0.3 and sosType=='Теплообменник':
        resultRevizia=f'В ФНП ОРПД данный случай не предусмотрен.\n\nЕсли рассмотреть случай с сосудами, то:\n Периодичность проведения НВО:\nОтветственным - раз в {nvoFNP[2][2]}\nСпец. организацией - раз в {nvoFNP[3][2]}\n\nПериодичность проведения ГИ:\nРаз в {nvoFNP[4][2]}'

    # РУА-93 и ИТНЭ-93
    elif ntd=='РУА' and skKorr<=0.1 and sosType=='Сосуд': # and srTRTS=='1 группа':
        resultRevizia=f'Для сосудов 1 группы\nНВО - раз в {nvoRUA01[0]}, ГИ - раз в {nvoRUA01[1]}\n\nДля сосудов 2 группы\nНВО - раз в {nvoRUA01[2]}, ГИ - раз в {nvoRUA01[3]}'
    elif ntd=='РУА' and 0.1<skKorr<=0.3 and sosType=='Сосуд': # and srTRTS=='1 группа':
        resultRevizia=f'Для сосудов 1 группы\nНВО - раз в {nvoRUA0103[0]}, ГИ - раз в {nvoRUA0103[1]}\n\nДля сосудов 2 группы\nНВО - раз в {nvoRUA0103[2]}, ГИ - раз в {nvoRUA0103[3]}'
    elif ntd=='РУА' and skKorr>0.3 and sosType=='Сосуд': # and srTRTS=='1 группа':
        resultRevizia=f'Для сосудов 1 группы\nНВО - раз в {nvoRUA03[0]}, ГИ - раз в {nvoRUA03[1]}\n\nДля сосудов 2 группы\nНВО - раз в {nvoRUA03[2]}, ГИ - раз в {nvoRUA03[3]}'
    elif ntd=='РУА' and skKorr<=0.1 and sosType=='Теплообменник': # and srTRTS=='1 группа':
        resultRevizia=f'Для теплообменников 1 группы\nНВО - раз в {nvoRUA01[4]}, ГИ - раз в {nvoRUA01[5]}\n\nДля теплообменников 2 группы\nНВО - раз в {nvoRUA01[6]}, ГИ - раз в {nvoRUA01[7]}'
    elif ntd=='РУА' and 0.1<skKorr<=0.3 and sosType=='Теплообменник': # and srTRTS=='1 группа':
        resultRevizia=f'Для теплообменников 1 группы\nНВО - раз в {nvoRUA0103[4]}, ГИ - раз в {nvoRUA0103[5]}\n\nДля теплообменников 2 группы\nНВО - раз в {nvoRUA0103[6]}, ГИ - раз в {nvoRUA0103[7]}'
    elif ntd=='РУА' and skKorr>0.3 and sosType=='Теплообменник': # and srTRTS=='1 группа':
        resultRevizia=f'Для теплообменников 1 группы\nНВО - раз в {nvoRUA03[4]}, ГИ - раз в {nvoRUA03[5]}\n\nДля теплообменников 2 группы\nНВО - раз в {nvoRUA03[6]}, ГИ - раз в {nvoRUA03[7]}'
    #ИТНЭ
    elif ntd=='ИТНЭ' and skKorr<=0.1 and sosType=='Сосуд':
        resultRevizia=f'{ntd}-93, Раздел 2, таблица 1\nДля сосудов при скорости коррозии {skKorr}<=0.1 мм/год\nНВО - раз в {nvoRUA01[0]}, ГИ - раз в {nvoRUA01[1]}'
    elif ntd=='ИТНЭ' and 0.1<skKorr<=0.3 and sosType=='Сосуд':
        resultRevizia=f'{ntd}-93, Раздел 2, таблица 1\nДля сосудов при скорости коррозии 0.1<{skKorr}<=0.3 мм/год\nНВО - раз в {nvoRUA0103[0]}, ГИ - раз в {nvoRUA0103[1]}'
    elif ntd=='ИТНЭ' and skKorr>0.3 and sosType=='Сосуд':
        resultRevizia=f'{ntd}-93, Раздел 2, таблица 1\nДля сосудов при скорости коррозии {skKorr}>0.3 мм/год\nНВО - раз в {nvoRUA03[0]}, ГИ - раз в {nvoRUA03[1]}'
    elif ntd=='ИТНЭ' and skKorr<=0.1 and sosType=='Теплообменник':
        resultRevizia=f'{ntd}-93, Раздел 2, таблица 2\nДля теплообменников при скорости коррозии {skKorr}<=0.1 мм/год\nНВО - раз в {nvoRUA01[4]}, ГИ - раз в {nvoRUA01[5]}'
    elif ntd=='ИТНЭ' and 0.1<skKorr<=0.3 and sosType=='Теплообменник':
        resultRevizia=f'{ntd}-93, Раздел 2, таблица 2\nДля теплообменников при скорости коррозии 0.1<{skKorr}<=0.3 мм/год\nНВО - раз в {nvoRUA0103[4]}, ГИ - раз в {nvoRUA0103[5]}'
    elif ntd=='ИТНЭ' and skKorr>0.3 and sosType=='Теплообменник':
        resultRevizia=f'{ntd}-93, Раздел 2, таблица 2\nДля теплообменников при скорости коррозии {skKorr}>0.3 мм/год\nНВО - раз в {nvoRUA03[4]}, ГИ - раз в {nvoRUA03[5]}'
    else:
        print('ошибка 3')
    return resultRevizia