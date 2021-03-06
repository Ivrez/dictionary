import os
import subprocess
import logging
import re
import random

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode, \
        InlineKeyboardMarkup, InlineKeyboardButton, \
        CallbackQuery
from aiogram.utils import executor

from adapter.adapter import Functions
from conf.conf import *

API_TOKEN = bot_api_token
logging.basicConfig(level=logging.DEBUG)

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

db = Functions()

help_message = '''\
dictionary bot
available commands:
/start
/quiz
'''

class Form(StatesGroup):
    quiz = State()

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.answer(help_message)

@dp.message_handler(commands=['quiz', 'next'])
async def quiz(message: types.Message):
    data = db.get_random_word(6)
    quiz_words = list()
    for word in data:
        quiz_words.append(word)
    selected_word = (quiz_words[random.randint(0, 5)])

    btn_words = list()
    for i in quiz_words:
        print(i)
        if i['word_eng'] == selected_word['word_eng']:
            btn_words.append(InlineKeyboardButton(i['word_eng'], callback_data='_correct'))
            continue
        btn_words.append(InlineKeyboardButton(i['word_eng'], callback_data='_not_correct'))

    inline_kb = InlineKeyboardMarkup()
    quit_btn = InlineKeyboardButton('quit', callback_data='quit')
    inline_kb.add(btn_words[0], btn_words[1], btn_words[2])
    inline_kb.add(btn_words[3], btn_words[4], btn_words[5])
    inline_kb.add(quit_btn)

    await message.answer(selected_word['word_rus'], reply_markup=inline_kb)

@dp.callback_query_handler(lambda c: c.data == '_correct', state="*")
async def process_callback_correct(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Правильно')
    await bot.send_message(callback_query.from_user.id, '/next')

@dp.callback_query_handler(lambda c: c.data == '_not_correct', state="*")
async def process_callback_not_correct(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Вы долбоеб')

@dp.callback_query_handler(lambda c: c.data == 'quit', state="*")
async def process_callback_quit(callback_query: types.CallbackQuery, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        await bot.send_message(callback_query.from_user.id, help_message)
    else:
        logging.info('Cancelling state %r', current_state)
        await state.finish()
        await bot.send_message(callback_query.from_user.id, help_message)
