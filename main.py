import telebot
from telebot import types

bot = telebot.TeleBot("867167395:AAE8915Oh6QMTq3UGT_KxdKnoCV9d-1V1cU")

name = ''
surname = ''
age = 0
rating = 0

@bot.message_handler(content_types=['text'])
def start(message):
    mes = str(message.text).lower
    if mes == '/help':
        bot.send_message(message.from_user.id,
        """
        Здравствуйте! Благодарим за использование нашего бота!
        Внизу Вы можете найти кнопку с символом '//',
        нажав не неё вы можете увидеть список доступных команд.
        Приятного использования. Вы можете оценить наш сервис с помощью команды //rate 
        """) 
    elif mes == '/banks':
        pass
    elif mes == '/ticket':
        pass
    elif mes == '/app':
        redirect_to('app', message)
    elif mes == '/site': 
        redirect_to('site', message)
    elif mes == '/rate':
        bot.register_next_step_handler(message, rate_app)
    else:
        bot.send_message(message.from_user.id, 'Я Вас не понимаю. Напишите /help')

def get_name(message): #получаем фамилию
    global name
    name = message
    bot.send_message(message.from_user.id, 'Какая у тебя фамилия?')
    bot.register_next_step_handler(message, get_surname)

def get_surname(message):
    global surname
    surname = message
    bot.send_message(message.from_user.id, 'Сколько тебе лет?')
    bot.register_next_step_handler(message, get_age)

def get_age(message):
    global age
    while age == 0: #проверяем что возраст изменился
        try:
            age = int(message) #проверяем, что возраст введен корректно
        except Exception:
            bot.send_message(message.from_user.id, 'Цифрами, пожалуйста')
    keyboard = set_YN_keyboard('get_age')
    question = 'Тебе '+ str(age) + ' лет, тебя зовут ' + name + ' ' + surname + '?'
    bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)

def rate_app(message):
    global rating
    bot.send_message(message.from_user.id, 'Оцените бота от 1 до 5')
    rating = 0
    while rating < 1 or rating > 5:
        try:
            rating = int(message)
        except Exception:
            bot.send_message(message.from_user.id, 'Введите корректные данные пожалуйста')
    keyboard = set_YN_keyboard('rate_app')
    question = 'Вы согласны с оценкой' + str(rating) + '?'
    bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)
    
    
def set_YN_keyboard(def_name):
    keyboard = types.InlineKeyboardMarkup() #наша клавиатура
    key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes'+ str(def_name)) #кнопка «Да»
    keyboard.add(key_yes) #добавляем кнопку в клавиатуру
    key_no= types.InlineKeyboardButton(text='Нет', callback_data='no' + str(def_name)) 
    keyboard.add(key_no)
    return keyboard

def redirect_to(link_type, message):
    if link_type == 'app':
        keyboard = types.InlineKeyboardMarkup()
        url_button = types.InlineKeyboardButton(text="Приложение на iOS", url="https://itunes.apple.com/ru/app/pages/id409201541?mt=12")
        keyboard.add(url_button)
        bot.send_message(message.chat.id, "Ссылка на приложение", reply_markup=keyboard)
    elif link_type == 'site':
        keyboard = types.InlineKeyboardMarkup()
        url_button = types.InlineKeyboardButton(text="Наш сайт", url="https://www.borrowlend.info")
        keyboard.add(url_button)
        bot.send_message(message.chat.id, "Ссылка на сайт", reply_markup=keyboard)



@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data[:3] == "yes":
        bot.send_message(call.message.chat.id, 'Спасибо!')
    elif call.data[:2] == "no":
        if call.data[3:] == "rate_app":
            bot.register_next_step_handler('', rate_app)
        elif call.data[3:] == "get_age":
            bot.register_next_step_handler('', get_age)
            


if __name__ == '__main__':
    bot.remove_webhook()
    bot.polling(none_stop=True)