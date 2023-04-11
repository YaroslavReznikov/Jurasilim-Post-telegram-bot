#!/usr/bin/end python3.9

import parsing
import telebot
import logging
from messages import *
from setup import bot


def main():
    pars = parsing.parsing_part()
    logger = telebot.logger
    logging.basicConfig(filename='logs.txt', level=logging.DEBUG,
                        format=' %(asctime)s - %(levelname)s - %(message)s')

    @bot.message_handler(commands=['new'])
    def send_new(message):
        links = pars.send_links_to_user()
        for _ in range(5):
            id, url, date, topic = next(links)
            bot.send_message(message.chat.id,
                             text=F"{date.strftime('%d.%m.%Y, %H:%M')}\n{topic.strip()}\n{url.strip()}")
            pars.update_sended(id)

    @bot.message_handler(commands=['check'])
    def admin_check(message):
        id, url, date, topic = next(pars.send_links_to_user())
        bot.send_message(message.chat.id, text=F"{date.strftime('%d.%m.%Y, %H:%M')}\n{topic.strip()}\n{url.strip()}")

    bot.polling(none_stop=True)

# 721184252
# 721184252
