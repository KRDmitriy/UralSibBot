import telebot
from telebot import types

def main_keyboard():
    try:
        keyboard = telebot.types.ReplyKeyboardMarkup()
        keyboard.row('Банки', 'Банкоматы')
        keyboard.row('Получить талон')
        keyboard.row('Сайт', 'Приложение')
        keyboard.row('Помощь', 'Оценить')
        return keyboard
    
    except:
        pass

def set_YN_keyboard(def_name):
    try:
        keyboard = types.InlineKeyboardMarkup() #наша клавиатура
        key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes'+ str(def_name)) #кнопка «Да»
        keyboard.add(key_yes) #добавляем кнопку в клавиатуру
        key_no= types.InlineKeyboardButton(text='Нет', callback_data='no' + str(def_name)) 
        keyboard.add(key_no)
        return keyboard
    
    except:
        pass

def set_NUM_keyboard(def_name, count):
    try:
        keyboard = types.InlineKeyboardMarkup()
        buttons = []

        for i in range(1, count + 1):
            buttons.append(types.InlineKeyboardButton(text=str(i), callback_data=str(def_name) + str(i)))

        if (count == 5):
            keyboard.row(buttons[0], buttons[1], buttons[2], buttons[3], buttons[4])
        else:
            for i in buttons:
                keyboard.add(i)
    
        return keyboard

    except:
        pass

def set_request_keyboard():
    try:
        keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        #button_phone = types.KeyboardButton(text="Отправить номер телефона", request_contact=True)
        button_geo = types.KeyboardButton(text="Отправить местоположение", request_location=True)
        button_cancel = types.KeyboardButton(text="Назад")
        #keyboard.add(button_phone, button_geo, button_cancel)
        keyboard.add(button_geo, button_cancel)
        return keyboard

    except:
        pass

def set_choose_action_keyboard():
    try:
        keyboard = telebot.types.ReplyKeyboardMarkup()
        """
        keyboard.row('Оплата интернета', 'Оплата телефона')
        keyboard.row('Оплата ЖКХ', 'Оплата телевидения')
        keyboard.row('Оплата обучения', 'Оплата штрафов')
        keyboard.row('Оплата налогов', 'Оплата телевидения')
        keyboard.row('Получение депозита (RUB)', 'Получение депозита (USD)')
        keyboard.row('Получение депозита (EUR)', 'Получение кредита')
        keyboard.row('Назад')
        """
        for i in range(9):
            keyboard.row('{0}:00'.format(i + 9), '{0}:30'.format(i + 9))
        keyboard.row('18:00', 'Назад')
        return keyboard

    except:
        pass

def set_rate_keyboard():
    try:
        keyboard = telebot.types.ReplyKeyboardMarkup()
        keyboard.row('Отлично!')
        keyboard.row('Просто огонь!')
        keyboard.row('Посоветую друзьям :) ')
        keyboard.row('Есть куда расти...')
        keyboard.row('Назад')
        return keyboard

    except:
        pass