import telebot, actions, keyboards, requests, json
from telebot import types
from message_handler import message_handler

bot = telebot.TeleBot("810876165:AAGhtlJ9ALfIII82Hx2V0-HvbXQLmUA71Ls")

@bot.message_handler(commands=['start'])
def start_message(message):
    actions.help(message.chat.id)

@bot.message_handler(content_types=['text'])
def start(message):
    message_handler(message)

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    try:
        if call.data[:3] == "yes":
            bot.send_message(call.message.chat.id, 'Спасибо!')

        elif call.data[:2] == "no":

            if call.data[2:] == "rate_app":
                actions.rate_app(call.message.chat.id)

        elif call.data[:8] == "rate_app":
            rating = int(call.data[-1])
            bot.delete_message(call.message.chat.id, call.message.message_id)
            bot.send_message(call.message.chat.id, 'Спасибо за оценку ' + str(rating) + ' !')

            answer = connnect_to_db("SELECT * FROM UserSession WHERE ChatID={0}".format(call.message.chat.id))
            data = json.loads(answer.text)
            if (data == []):
                answer = connnect_to_db("INSERT INTO UserSession (ChatID, Rating, Reason, IsTicket, Result) VALUES({0},{1},{2},{3},{4})".format(call.message.chat.id, rating, '', 0, ''))
            else:
                answer = connnect_to_db("UPDATE UserSession SET Rating={0} where ChatID={1}".format(rating, call.message.chat.id))

            actions.get_comment(call.message.chat.id)

        elif call.data[:3] == 'add':
            if call.data[3:] == 'comment':
                bot.send_message(call.message.chat.id, 'Пожалуйста напишите Ваш отзыв', reply_markup=keyboards.set_rate_keyboard())
                bot.register_next_step_handler(call.message, actions.reg_comment)
                bot.delete_message(call.message.chat.id, call.message.message_id)
    except:
        pass
    
@bot.message_handler(content_types=['location'])
def get_location_for(message):
    actions.search(message, message.location)

@bot.message_handler(content_types=['contact'])
def get_contact(message):
    bot.send_message(message.chat.id, str(message.contact), reply_markup=keyboards.main_keyboard())

def connnect_to_db(request_string):
    try:
        return requests.get("https://www.aerothedeveloper.ru/api/UserSessions?query=" + request_string)
    except:
        pass

def post_to_db(request_string):
    try:
        return requests.post("https://www.aerothedeveloper.ru/api/UserSessions", data = request_string.encode("utf-8"))
    except:
        pass

if __name__ == '__main__':
    try:
        bot.remove_webhook()  
        bot.polling(none_stop=True)

    except:
        pass