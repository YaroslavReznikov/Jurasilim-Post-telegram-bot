import logging
import parsing
from aiogram import Bot, Dispatcher, executor, types
import requests

token = "5744717544:AAE0s0J_X8zz1EW3zexj1dW4tYdsoTVCCxY"
bot = Bot(token)
dp = Dispatcher(bot)


pars = parsing.parsing_part()
pars.get_links("https://rss.jpost.com/rss/rssfeedsfrontpage.aspx")
pars.database_sending()
#@dp.message_handler(commands=['help', 'start'])
#async def send_welcome_message(mesage: types.Message):
#    await mesage.reply("Hi")


#if __name__ == '__main__':
    #executor.start_polling(dp)
