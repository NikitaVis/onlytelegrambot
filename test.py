@bot.message_handler(content_types=["text"])
def send_simple_message(id_chat,message):
    bot.send_message(id_chat, message)


def obtain_checked_and_no_responsed_data():
    conn = sqlite3.connect('main_db.db')
    cursor = conn.cursor()
    data = cursor.execute("SELECT * FROM request_state_response_data WHERE is_checked = 1 and is_send_to_user = 0")
    data = data.fetchall()[0]
    print (data)
    send_simple_message(data[2], data[3])
    conn.commit()
