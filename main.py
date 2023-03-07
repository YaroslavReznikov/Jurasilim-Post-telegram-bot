#!/usr/bin/end python3.9


import parsing
import telebot
import schedule

token = "5744717544:AAE0s0J_X8zz1EW3zexj1dW4tYdsoTVCCxY"
bot = telebot.TeleBot(token)

pars = parsing.parsing_part()

schedule.every(120).seconds.do(pars.get_links)
pars.get_links()
while True:
    schedule.run_pending()
    @bot.message_handler(commands=['new'])
    def send_new(message):
        links = pars.send_links_to_user()
        for _ in range(5):
            id, url, date, topic = next(links)
            bot.send_message(message.chat.id, text=F"{date.strftime('%d: %m: %Y, %H:%M')}'\n' {topic} '\n' {url}")
            pars.update_sended(id)


    @bot.message_handler(commands=['check'])
    def admin_check(message):
        id, url, date, topic = next(pars.send_links_to_user())
        bot.send_message(message.chat.id, text=F"{date.strftime('%d: %m: %Y, %H:%M')}'\n' {topic} '\n' {url}")


    bot.polling(none_stop=True)
