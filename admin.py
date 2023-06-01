#import pandas as pd
#import datetime as dt
#import io

from aiogram import Dispatcher, types
#from aiogram.dispatcher import FSMContext
#from aiogram.dispatcher.filters import Text
#from aiogram.dispatcher.filters.state import State, StatesGroup
#from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from sqlite_db import sql_read
import admin_kb

from create_bot import bot, my_status

idd = None

# Get Moderator Id 
# @dp.message_handler(commands=['moderator'], is_chat_admin=True)
async def moderator_command(message: types.Message):
    global idd
    idd = message.from_user.id
    await bot.send_message(message.from_user.id, 'What do you want Sir Yandex?', reply_markup=admin_kb.button_case_admin)
    await message.delete()


# Start Menu Load Dialog
# @dp.message_handler(commands='statistics', state=None)
async def cm_descstat(message : types.Message):
    if message.from_user.id == idd:
        df = sql_read()
        sss = df.describe(include='object').to_string()
        #print(df.describe(include='object'))
        await bot.send_message(message.from_user.id, sss, reply_markup=admin_kb.button_case_admin)

async def cm_itemstat(message : types.Message):
    if message.from_user.id == idd:
        #df = sql_read()
        num_rows = df.shape[0]
        bbuf = 'Collected: ' + str(num_rows) + ' rows.'
        await bot.send_message(message.from_user.id, bbuf, reply_markup=admin_kb.button_case_admin)
# Handlers Registration
def register_handlers_admin(dp : Dispatcher):
    dp.register_message_handler(cm_descstat, commands='descstat')
    dp.register_message_handler(cm_itemstat, commands='itemstat')
    dp.register_message_handler(moderator_command, commands=['moderator'], is_chat_admin=True)