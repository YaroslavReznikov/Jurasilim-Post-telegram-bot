#!/usr/bin/end python3.9


import parsing
import telebot

try:
    token = "5744717544:AAE0s0J_X8zz1EW3zexj1dW4tYdsoTVCCxY"
    bot = telebot.TeleBot(token)
    bot.send_message(721184252, text='I am launched')
except:
    print("already works")
else:
    pars = parsing.parsing_part()
    @bot.message_handler(commands=['new'])
    def send_new(message):
        links = pars.send_links_to_user()
        for _ in range(5):
            id, url, date, topic = next(links)
            bot.send_message(message.chat.id, text=F"{date.strftime('%d.%m.%Y, %H:%M')}\n{topic.strip()}\n{url.strip()}")
            pars.update_sended(id)



    @bot.message_handler(commands=['check'])
    def admin_check(message):
        id, url, date, topic = next(pars.send_links_to_user())
        bot.send_message(message.chat.id, text=F"{date.strftime('%d.%m.%Y, %H:%M')}\n{topic.strip()}\n{url.strip()}")

    bot.polling(none_stop=True)

#721184252
#721184252