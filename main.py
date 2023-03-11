#!/usr/bin/end python3.9


import parsing
import telebot
from time import time


token = "5744717544:AAE0s0J_X8zz1EW3zexj1dW4tYdsoTVCCxY"
bot = telebot.TeleBot(token)

pars = parsing.parsing_part()

last_time = time()
#pars.get_links()


@bot.message_handler(commands=['new'])
def send_new(message):
    links = pars.send_links_to_user()
    for _ in range(5):
        id, url, date, topic = next(links)
        bot.send_message(message.chat.id, text=F"{date.strftime('%d.%m.%Y, %H:%M')}\n{topic.strip()}\n{url.strip()}")
        pars.update_sended(id)



@bot.message_handler(commands=['check'])
def admin_check(message):
    print('send_first')

    id, url, date, topic = next(pars.send_links_to_user())
    bot.send_message(message.chat.id, text=F"{date.strftime('%d.%m.%Y, %H:%M')}\n{topic.strip()}\n{url.strip()}")
