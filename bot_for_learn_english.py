import os
import re
import asyncio
import logging

from random import randint

from aiogram import Bot, types
from aiogram.types import ParseMode
from aiogram.utils.markdown import text
from aiogram.dispatcher import Dispatcher
from aiogram.types.message import ContentType
from aiogram.utils.executor import start_webhook

from db import init_tables
from db import add_word
from db import count_words
from db import list_all_words


# Config for bot on heroku
TOKEN = os.environ['TOKEN']
WEBHOOK_HOST = 'https://telegram-heroku-bot-zark.herokuapp.com'  # name your app
WEBHOOK_PATH = '/webhook/'
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"
WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = os.environ.get('PORT')


# Create log string
logging.basicConfig(level=logging.INFO)

# Create dispatcher and bot 
# loop = asyncio.get_event_loop()
bot = Bot(token=TOKEN, parse_mode='HTML')
dp = Dispatcher(bot)


# Create function which process connand /start
@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply('Hi bro! Learn english words with me.')


# Create function which process connand /help
@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    msg = text('The next commands to help you:', '/add', '/learn', sep='\n')
    # await message.reply(msg, parse_mode=ParseMode.HTML)
    await message.reply(msg)


# Create function which process words to write where to dict
@dp.message_handler(commands=['add'])
async def process_add_new_word(message: types.Message):
    regexp = r'[^(/add)](.+)'
    word = re.findall(regexp, message['text'])
    arr = [i for i in word[0].split(' - ')]
    add_word(user_id=message.chat.id, word=arr[0], translate=arr[1])
    msg = f'Successful add {word[0]}'
    await bot.send_message(message.chat.id, msg, reply_to_message_id=message.message_id)


# Create function which process words to learn from dict
@dp.message_handler(commands=['learn'])
async def process_learn_word(message: types.Message):
    words = list_all_words(user_id=message.chat.id)
    r = randint(0, len(words) - 1)
    msg = f'{words[r][2]} - {words[r][3]}'
    await bot.send_message(message.chat.id, msg, reply_to_message_id=message.message_id)


# Create function which process any message from user
@dp.message_handler(content_types=ContentType.ANY)
async def unknown_message(msg: types.Message):
    message_text = text('What the fuck is this?')
    await msg.reply(message_text)


# Create the function to startup my bot
async def on_startup(dp):
    await bot.set_webhook(WEBHOOK_URL)


# Create the function to shutdown my bot
async def on_shutdown(dp):
    await bot.close()


# Main script
if __name__ == '__main__':
    init_tables()
    start_webhook(dispatcher=dp, webhook_path=WEBHOOK_PATH,
                  on_startup=on_startup, on_shutdown=on_shutdown,
                  host=WEBAPP_HOST, port=WEBAPP_PORT)
