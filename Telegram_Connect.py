# -*- coding: utf-8 -*-
import telebot
import time
import sqlite3
import datetime

token = '753647739:AAFWJwRFy1b9iDE3UKlq6bk6aoX5janRjck'

bot = telebot.TeleBot(token)

def clear_number (number):
    number = str(number).replace("(","").replace(")","").replace("-","").replace('+7','8')
    return number

@bot.message_handler(content_types=["text"])
def insert_new_message_in_sqlite(message):
    print (message.text)
    if message.text != '/start':
        time_request_from_user = str(datetime.datetime.now())
        origin_phone_number_to_check = str(message.text)
        good_number_to_check = str(clear_number (message.text))
        id_chat = str(message.chat.id)
        is_checked = '0'
        is_send_to_user = '0'

        conn = sqlite3.connect('main_db.db')
        cursor = conn.cursor()

        count = len(cursor.execute("SELECT * FROM request_state_response_data WHERE is_checked = 0 ").fetchall())
        count=count+1
        print(count)

        cursor.execute("INSERT INTO request_state_response_data (time_request_from_user,id_chat,origin_phone_number_to_check,good_number_to_check,is_checked,is_send_to_user,time_send_to_user, que_num) "
                                              "VALUES ('"+time_request_from_user+"','"+id_chat+"','"+origin_phone_number_to_check+"','"+good_number_to_check+"','"+is_checked+"','"+is_send_to_user+"','no time','"+str(count)+"')")
        conn.commit()
        conn.close()
        bot.send_message(id_chat, "Вы "+str(count)+"-й в очереди на проверку номера")
    else:
        welcome_msg = u"Бот рад приветствовать Вас. Введите номер телефона человека о котором желали бы узнать всё..."
        bot.send_message(message.chat.id, welcome_msg)

def obtain_not_checked_phone_number ():
    returnDict ={}

    conn = sqlite3.connect('main_db.db')
    cursor = conn.cursor()

    data = cursor.execute("SELECT * FROM request_state_response_data WHERE is_checked = 0 and is_send_to_user = 0").fetchall()
    for one_corteg in data:
        returnDict[one_corteg[2]] = one_corteg[4]

    conn.commit()
    conn.close()

    print(returnDict)
    return returnDict



def  mainDef():
    bot.polling(none_stop=True)

if __name__ == '__main__':
    mainDef()






