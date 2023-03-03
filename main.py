import parsing
import telebot
import time

token = "5744717544:AAE0s0J_X8zz1EW3zexj1dW4tYdsoTVCCxY"
bot = telebot.TeleBot(token)
#dp = Dispatcher(bot)

#start = time.perf_counter()
pars = parsing.parsing_part()

links = pars.send_links_to_user()

@bot.message_handler(commands=['new'])
def send_new(message):
    for _ in range(5):
        id, url = next(links)
        bot.send_message(message.chat.id, text=F"{url}")
        pars.update_sended(id)

bot.polling(none_stop=True)