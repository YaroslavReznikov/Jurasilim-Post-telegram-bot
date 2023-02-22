import telebot
import requests

token = "5744717544:AAE0s0J_X8zz1EW3zexj1dW4tYdsoTVCCxY"
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['help', 'start'])
def send_welcome_message(mesage):
    bot.reply_to(mesage, 'I am working')
