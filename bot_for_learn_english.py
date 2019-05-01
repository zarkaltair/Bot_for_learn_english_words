import asyncio
import logging
import re
import numpy as np

from aiogram import Bot, types
from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher
from aiogram.types.message import ContentType
from aiogram.utils.markdown import text, bold, italic, code, pre
from aiogram.types import ParseMode, InputMediaPhoto, InputMediaVideo, ChatActions

from config import TOKEN
from config import PROXY_URL


# Create log string
logging.basicConfig(format=u'%(filename)s [ LINE:%(lineno)+3s ]#%(levelname)+8s [%(asctime)s]  %(message)s', level=logging.INFO)

# pass to bot token and proxy url
bot = Bot(token=TOKEN, proxy=PROXY_URL)
dp = Dispatcher(bot)


# Create function which process connand /start
@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply('Hi bro! Learn english words with me.')


# Create function which process connand /help
@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    msg = text('The next commands to help you:', '/add', '/learn', sep='\n')
    await message.reply(msg, parse_mode=ParseMode.HTML)


arr_with_dict_of_words = [['learn - учить'], ['insted of - вместо'], ['otherwise - иначе']]


# Create function which process words to write where to dict
@dp.message_handler(commands=['add'])
async def process_add_new_word(message: types.Message):
    regexp = r'[^(/add)](.+)'
    word = re.findall(regexp, message['text'])
    words = word[0]  + '\n'
    print(words)
    file_with_words = open('file_with_words.txt', 'a')
    file_with_words.write(words)
    file_with_words.close()
    msg = f'Successful add {words}'
    await bot.send_message(message.chat.id, msg, reply_to_message_id=message.message_id)


# Create function which process words to learn from dict
@dp.message_handler(commands=['learn'])
async def process_learn_word(message: types.Message):
    file = open('file_with_words.txt', 'r')
    arr_with_words = [line.strip() for line in file]
    msg = np.random.choice(arr_with_words)
    file.close()
    await bot.send_message(message.chat.id, msg, reply_to_message_id=message.message_id)


# Create function which process any message from user
@dp.message_handler(content_types=ContentType.ANY)
async def unknown_message(msg: types.Message):
    message_text = text('What the fuck is this?')
    await msg.reply(message_text, parse_mode=ParseMode.MARKDOWN)


if __name__ == '__main__':
    executor.start_polling(dp)