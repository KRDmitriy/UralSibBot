import telebot
from telebot import types
import main, keyboards, requests, sqlite3, json
from MapsAndUsers import RunPrograme, RunProgramWithThreeBanks
import qrcode, io

def help(chat_id):
    try:
        main.bot.send_message(chat_id,
            'Здравствуйте! Благодарим за использование нашего бота! ' +
            "Внизу находится кнопка меню, " +
            'нажав на неё, Вы сможете увидеть список доступных команд. ' +
            'Приятного использования! Вы можете оценить наш сервис с помощью команды /rate или кнопки "Оценить"',
            reply_markup=keyboards.main_keyboard())
    except:
        pass

def rate_app(chat_id):
    try:
        question = 'Оцените бота от 1 до 5'
        keyboard = keyboards.set_NUM_keyboard('rate_app', 5)
        main.bot.send_message(chat_id, text=question, reply_markup=keyboard)
    except:
        pass
        

def redirect_to(link_type, message):
    try:
        if link_type == 'app':
            keyboard = types.InlineKeyboardMarkup()
            ios_button = types.InlineKeyboardButton(text="Приложение на iOS", url="https://itunes.apple.com/ru/app/мобильный-банк-уралсиб/id808733030?mt=8")
            keyboard.add(ios_button)
            droid_button = types.InlineKeyboardButton(text="Приложение на Android", url="https://play.google.com/store/apps/details?id=ru.bankuralsib.mb.android")
            keyboard.add(droid_button)
            main.bot.send_message(message.chat.id, "Ссылка на приложение", reply_markup=keyboard)
        elif link_type == 'site':
            keyboard = types.InlineKeyboardMarkup()
            url_button = types.InlineKeyboardButton(text="Наш сайт", url="https://www.uralsib.ru/")
            keyboard.add(url_button)
            main.bot.send_message(message.chat.id, "Ссылка на сайт", reply_markup=keyboard)
    except:
        pass

def get_comment(chat_id):
    try:
        keyboard = types.InlineKeyboardMarkup()
        key_add = types.InlineKeyboardButton(text='Добавить отзыв', callback_data='addcomment')
        keyboard.add(key_add)
        main.bot.send_message(chat_id, 'Желаете прокомментировать?', reply_markup=keyboard)
    except:
        pass

def get_ticket(chat_id):
    try:
        main.bot.send_message(chat_id, 'Введите код талона в формате: kod:код вашего купона',
            reply_markup=keyboards.main_keyboard())
    except:
        pass

def check_ticket(message, chat_id):
    try:
        ticket = message[4:]
        main.bot.send_message(chat_id, 'Код талона: ' + str(ticket), reply_markup=keyboards.main_keyboard())

        url = "https://aerothedeveloper.ru/api/couponcodes?code=" + str(ticket).upper()
        m_answer = requests.get(url)
        couponData = json.loads(m_answer.text)

        answer = main.connnect_to_db("SELECT * FROM UserSession WHERE ChatID={0}".format(chat_id))
        data = json.loads(answer.text)
        if (data == []):
            answer = main.post_to_db("INSERT INTO UserSession (ChatID, Rating, Reason, IsTicket, Result) VALUES({0},{1},'{2}',{3},'{4}')".format(chat_id, 0, '', 0, m_answer.text))
        else:
            answer = main.post_to_db("UPDATE UserSession SET Result='{0}' where ChatId={1}".format(m_answer.text, chat_id))

        if couponData != []:
            active = couponData["CouponCodeStatus"]
            if (active == 1):
                rate_app(chat_id)
            else:
                main.bot.send_message(chat_id, 'Вы уже оценили это посещение!', reply_markup=keyboards.main_keyboard())
        else:
            main.bot.send_message(chat_id, 'Некорректный код оценки талон', reply_markup=keyboards.main_keyboard())

    except:
        pass

def reg_comment(message):
    try:
        answer = main.connnect_to_db("SELECT * FROM UserSession WHERE ChatID={0}".format(message.chat.id))
        data = json.loads(answer.text)
        res = data[0]["Result"]
        rating = data[0]["Rating"]

        res = json.loads(res)

        url = "https://aerothedeveloper.ru/api/coupons?ID=" + str(res["CouponID"])

        answer = requests.get(url)
        data = json.loads(answer.text)

        send = {
            "ID": 0,
            "UserID": 1, 
            "CouponID": data["ID"],
            "OfficeID": data["OfficeID"],
            "Mark": rating,
            "Comment": str(message.text),
        }

        url = "https://aerothedeveloper.ru/api/assesments"
        answer = requests.post(url, json.dumps(send))

        main.bot.delete_message(message.chat.id, message.message_id - 1)
        main.bot.send_message(message.chat.id, 'Спасибо! Ваш отзыв очень важен для нас!', reply_markup=keyboards.main_keyboard())
    
    except:
        pass

def get_user_data(message):
    try:
        keyboard = keyboards.set_request_keyboard()
        main.bot.send_message(message.chat.id, "Отправьте ваши данные!", reply_markup=keyboard)
        main.bot.register_next_step_handler(message, main.get_location_for)
    except:
        pass
    
def search(message, params):
    try:
        main.bot.send_message(message.chat.id, "Ищем отделение(я)!", reply_markup=keyboards.main_keyboard())
        point = []
        
        data = str(params)

        k = data.index("'latitude':")
        point.append(float(data[k + 12:-1]))
        k = data.index(', ')
        point.append(float(str(params)[14:k]))

        answer = main.connnect_to_db("SELECT * FROM UserSession WHERE ChatID={0}".format(message.chat.id))

        is_ticket = json.loads(answer.text)[0]["IsTicket"]

        if (is_ticket == 1):
            cb, address, id = RunPrograme(point, "https://aerothedeveloper.ru/api/office")
            main.bot.send_location(message.chat.id, cb[0], cb[1])
            main.bot.send_message(message.chat.id, str(address).title(), reply_markup=keyboards.main_keyboard())
            create_ticket(message, id, address)
        else:
            cb, address, id = RunProgramWithThreeBanks(point, "https://aerothedeveloper.ru/api/office")
            for i in range(3):
                main.bot.send_location(message.chat.id, cb[i][0], cb[i][1])
                main.bot.send_message(message.chat.id, str(address[i]).title(), reply_markup=keyboards.main_keyboard())

    except:
        pass


def create_ticket(message, id, address):
    try:
        if id == -1:
            get_user_data(message)
        else:
            answer = main.connnect_to_db("SELECT * FROM UserSession WHERE ChatID={0}".format(message.chat.id))
            reason = json.loads(answer.text)[0]["Reason"]

            office_id = str(id)
            office_address = address
            ticket = str('{"ID":2,"UserID":0,"OfficeID":' + office_id + ',"CreationDate":"2019-04-27T23:05:51.193","VisitTime":"2019-04-27T23:05:51.193","OfficeAddress":"' + office_address + '","ServiceType":"' + reason + '","CouponStatus":0}').encode('utf8')
            url = "https://aerothedeveloper.ru/api/coupons"

            answer = requests.post(url, data=ticket)

            data = json.loads(answer.text)
            id = data["ID"]
            info = str('Талон № ' + str(id) + ' получен! Офис расположен по адресу ' + office_address + '. Время посещения: ' + reason +'.')

            main.bot.send_message(message.chat.id, info, reply_markup=keyboards.main_keyboard())

            url = "https://aerothedeveloper.ru/api/couponcodes?couponID=" + str(id)

            answer = requests.get(url)
            data = json.loads(answer.text)
            code = data["Code"]

            main.bot.send_message(message.chat.id, 'Используйте этот код: ' + code + ' для оценки оказанной услуги с помощью функции /rate', reply_markup=keyboards.main_keyboard())

            answer = main.post_to_db("UPDATE UserSession SET IsTicket=0 where ChatId={0}".format(message.chat.id))

            #Неудачная попытка отправлять QR-код с номером купона
            """text = str(id)
            img = qrcode.make(text)
            io_data = io.BytesIO()
            img.save(io_data, 'png')
            data = io_data.getvalue()
            with open('qr_code.png', 'wb') as f:
                f.write(data)

            main.bot.send_photo(message.chat.id, final_img)"""
    
    except:
        pass