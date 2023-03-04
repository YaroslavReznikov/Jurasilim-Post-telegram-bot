import parsing
import telebot
import time

token = "5744717544:AAE0s0J_X8zz1EW3zexj1dW4tYdsoTVCCxY"
bot = telebot.TeleBot(token)
#dp = Dispatcher(bot)

#start = time.perf_counter()
pars = parsing.parsing_part()
#pars.get_links("https://rss.jpost.com/rss/rssfeedsfrontpage.aspx")
links = pars.send_links_to_user()
#pars.feel_the_rss_database_database()

#pars.get_links()
@bot.message_handler(commands=['new'])
def send_new(message):
    for _ in range(5):
        url, date, id, topic = next(links)
        bot.send_message(message.chat.id, text=F"{date.strftime('%d: %m: %Y, %H:%M'), topic,url}")
        #pars.update_sended(id)



bot.polling(none_stop=True)