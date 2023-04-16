#!/usr/bin/end python3.9

import parsing
import telebot
import logging
from setup import bot


def main():
    pars = parsing.ParsingPart()
    logging.basicConfig(filename='logs.txt', level=logging.DEBUG,
                        format=' %(asctime)s - %(levelname)s - %(message)s')

    @bot.message_handler(commands=['new'])
    def send_new(message):
        links = pars.send_links_to_user(message.chat.id)
        for _ in range(5):
            users_id, url, date, topic = next(links)
            bot.send_message(message.chat.id,
                             text=F"{date.strftime('%d.%m.%Y, %H:%M')}\n{topic.strip()}\n{url.strip()}")

    @bot.message_handler(commands=['check'])
    def admin_check(message):
        users_id, url, date, topic = next(pars.send_links_to_user(message.chat.id))
        bot.send_message(message.chat.id, text=F"{date.strftime('%d.%m.%Y, %H:%M')}\n{topic.strip()}\n{url.strip()}")

    bot.polling(none_stop=True)
