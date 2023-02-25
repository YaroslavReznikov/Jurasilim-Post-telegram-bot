import logging
import parsing
from aiogram import Bot, Dispatcher, executor, types
import time
import requests

token = "5744717544:AAE0s0J_X8zz1EW3zexj1dW4tYdsoTVCCxY"
bot = Bot(token)
dp = Dispatcher(bot)

start = time.perf_counter()
pars = parsing.parsing_part()

pars.get_links("main_page.aspx")
pars.database_sending()
print("it took", time.perf_counter() - start )
#@dp.message_handler(commands=['help', 'start'])
#async def send_welcome_message(mesage: types.Message):
#    await mesage.reply("Hi")


#if __name__ == '__main__':
    #executor.start_polling(dp)
