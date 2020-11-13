import os
import subprocess
import logging
import re

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode, \
        InlineKeyboardMarkup, InlineKeyboardButton, \
        CallbackQuery
from aiogram.utils import executor

from conf.conf import *

API_TOKEN = bot_api_token
logging.basicConfig(level=logging.DEBUG)

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

commands = ['help', 'add_word', 'search_dictionary', 'show_dictionary', 'rules']
help_message = '''\
dictionary bot
available commands:
/start
/search
/quiz
/rules
'''

class Form(StatesGroup):
    quiz = State()

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.answer(help_message)

@dp.message_handler(commands=['quiz'])
async def send_welcome(message: types.Message):
    await Form.quiz.set()
    quit_btn = InlineKeyboardButton('quit', callback_data='quit_btn')
    inline_kb = InlineKeyboardMarkup()
    inline_kb.add(quit_btn)
    await message.answer("input some text here", reply_markup=inline_kb)


@dp.callback_query_handler(lambda c: c.data == 'quit_btn', state="*")
async def process_callback_quit(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    current_state = await state.get_state()
    if current_state is None:
        return

    logging.info('Cancelling state %r', current_state)
    await state.finish()
    await bot.send_message(callback_query.from_user.id, help_message)
