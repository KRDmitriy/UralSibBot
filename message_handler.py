import telebot, main, actions, keyboards, json

def message_handler(message, mes=''):
    commands = ['оплата интернета', 'оплата телефона', 'оплата жкх', 'оплата телевидения',
            'оплата обучения', 'оплата штрафов', 'оплата налогов', 'оплата телевидения',
            'получение депозита (rub)', 'получение депозита (usd)', 'получение депозита (eur)', 'получение кредита']

    times = ['9:00', '9:30', '10:00', '10:30', '11:00', '11:30', '12:00', '12:30', '13:00', '13:30',
                '14:00', '14:30', '15:00', '15:30', '16:00', '16:30', '17:00', '17:30', '18:00',
    ]

    command_list = {
        "find":"bank", "bank":"bank", "find bank":"bank", "банк":"bank",
        "найти банк":"bank", "ближайший":"bank", ",ближайший банк":"bank",
        "урал сиб банк":"bank", "уралсиб банк":"bank", "уралсиббанк":"bank",
        "банкомат":"atm","get money":"atm","money":"atm",
        "снять деньги":"atm","положить деньги":"atm","терминал":"atm",
        "наличность":"atm","отправить деньги":"atm","сайт":"site","site":"site",
        "web":"site","web-site":"site","вебсайт":"site","веб-сайт":"site","емейл":"site",
        "email":"site","портал":"site","зайти на сайт":"site",
        "официальный сайт":"site","яндекс":"site","приложение":"app",
        "appware":"app","программа":"app","мобильное приложение":"app","оценить":"mark",
        "оценка":"mark","рекомендация":"mark","порекомендовать":"mark","оплатить":"ticket",
        "pay":"ticket","ЖКХ":"ticket","комуналка":"ticket","налог":"ticket","налоги":"ticket",
        "интернет":"ticket","телевидение":"ticket","задолженность":"ticket","квартплата":"ticket",
        "газ":"ticket","недвижимость":"ticket","долги":"ticket","ссылка":"site","ссылочка":"site",
    }

    if (mes == ''):
        mes = str(message.text).lower()

    if mes == 'банки' or mes == '/banks' or mes == 'banks' or mes == 'bank':

        answer = main.connnect_to_db("SELECT * FROM UserSession WHERE ChatID={0}".format(message.chat.id))

        data = json.loads(answer.text)
        if data == []:
            answer = main.post_to_db("INSERT INTO UserSession (ChatID, Rating, Reason, IsTicket, Result) VALUES({0},{1},'{2}',{3},'{4}')".format(message.chat.id, 0, '', 0, ''))
        else:
            answer = main.post_to_db("UPDATE UserSession SET IsTicket=0 WHERE ChatID={0}".format(message.chat.id))

        actions.get_user_data(message)

    elif mes == 'банкоматы' or mes == '/atms' or mes == 'atms':

        answer = main.connnect_to_db("SELECT * FROM UserSession WHERE ChatID={0}".format(message.chat.id))

        data = json.loads(answer.text)
        if data == []:
            answer = main.post_to_db("INSERT INTO UserSession (ChatID, Rating, Reason, IsTicket, Result) VALUES({0},{1},'{2}',{3},'{4}')".format(message.chat.id, 0, '', 0, ''))
        else:
            answer = main.post_to_db("UPDATE UserSession SET IsTicket=0 WHERE ChatID={0}".format(message.chat.id))

        actions.get_user_data(message)

    elif mes == 'получить талон' or mes == '/ticket' or mes == 'ticket':
        main.bot.send_message(message.chat.id, 'Выберите планируемое время обращения:', reply_markup=keyboards.set_choose_action_keyboard())

        answer = main.connnect_to_db("SELECT * FROM UserSession WHERE ChatID={0}".format(message.chat.id))

        data = json.loads(answer.text)
        if data == []:
            answer = main.post_to_db("INSERT INTO UserSession (ChatID, Rating, Reason, IsTicket, Result) VALUES({0},{1},'{2}',{3},'{4}')".format(message.chat.id, 0, '', 1, ''))
        else:
            answer = main.post_to_db("UPDATE UserSession SET IsTicket=1 WHERE ChatID={0}".format(message.chat.id))


    elif mes == 'сайт' or mes == '/site' or mes == 'site': 
        actions.redirect_to('site', message)

    elif mes == 'приложение' or mes == '/app' or mes == 'app':
        actions.redirect_to('app', message)

    elif mes == 'помощь' or mes == '/help' or mes == 'help':
        actions.help(message.chat.id) 

    elif mes == 'оценить' or mes == '/rate' or mes == 'rate':
        actions.get_ticket(message.chat.id)

    elif mes[:4] == 'kod:':
        actions.check_ticket(mes, message.chat.id)

    elif mes in times:
        
        answer = main.connnect_to_db("SELECT * FROM UserSession WHERE ChatID={0}".format(message.chat.id))

        data = json.loads(answer.text)
        if data == []:
            answer = main.post_to_db("INSERT INTO UserSession (ChatID, Rating, Reason, IsTicket, Result) VALUES({0},{1},N'{2}',{3},N'{4}')".format(message.chat.id, 0, str(message.text), 1, ''))
        else:
            answer = main.post_to_db("UPDATE UserSession SET Reason=N'" + message.text + "' WHERE ChatID=" + str(message.chat.id))
        
        actions.create_ticket(message, -1, '')

    elif mes in command_list.keys():
        message_handler(message, command_list[mes])

    elif mes == 'назад':
        main.bot.send_message(message.chat.id, 'Действие отменено',
            reply_markup=keyboards.main_keyboard())

    else:
        main.bot.send_message(message.chat.id, 'Я Вас не понимаю! /help ',
            reply_markup=keyboards.main_keyboard())
