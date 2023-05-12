#!/usr/bin/end python3.9

import parsing
import logging
from setup import bot


def main():
    pars = parsing.ParsingPart()
    logging.basicConfig(filename='logs.txt', level=logging.DEBUG,
                        format=' %(asctime)s - %(levelname)s - %(message)s')

    @bot.message_handler(func=lambda message: True)
    def message_handler(message):
        parts = message.text.split(' ', 2)
        command = parts[0].lower()
        if command == '/add_new_news':
            rss_url = parts[1] if len(parts) > 1 else ''
            prio = parts[2] if len(parts) > 2 else 0
            try:
                pars.add_new_source(rss_url, message.chat.id, prio)
            except:
                bot.reply_to(message, 'Some thing wrong with the url')
        if command == '/new':
            send_new(message)
        if command == '/check':
            admin_check(message)
        else:
            help(message)

    def help(message):
        pass

    def send_new(message):
        links = pars.find_links_for_user(message.chat.id, 5)
        for url, date, news_id, channels_row, topic in links:
            pars.add_url(message.chat.id, news_id)
            bot.send_message(message.chat.id,
                             text=F"{date.strftime('%d.%m.%Y, %H:%M')}\n{topic.strip()}\n{url.strip()}")

    def admin_check(message):
        links = pars.find_links_for_user(message.chat.id, 1)
        for url, date, news_id, channels_row, topic in links:
            pars.add_url(message.chat.id, news_id)
            bot.send_message(message.chat.id,
                             text=F"{date.strftime('%d.%m.%Y, %H:%M')}\n{topic.strip()}\n{url.strip()}")
            pars.get_links()
    bot.polling(none_stop=True)
