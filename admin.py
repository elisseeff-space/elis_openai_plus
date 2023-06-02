from aiogram import Dispatcher, types
from sqlite_db import sql_read, sql_read_tokens
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
async def cm_tokens_used(message : types.Message):
    if message.from_user.id == idd:
        res = sql_read_tokens()
        print(res)
        await bot.send_message(message.from_user.id, res, reply_markup=admin_kb.button_case_admin)

async def cm_chats(message : types.Message):
    if message.from_user.id == idd:
        bbuf = 'Chats in connection: ' + str(len(my_status.group_messages)) + '.'
        await bot.send_message(message.from_user.id, bbuf, reply_markup=admin_kb.button_case_admin)

async def cm_voice_records(message : types.Message):
    if message.from_user.id == idd:
        df = sql_read()
        num_rows = df.shape[0]
        bbuf = 'Collected: ' + str(num_rows) + ' rows.'
        await bot.send_message(message.from_user.id, bbuf, reply_markup=admin_kb.button_case_admin)

# Handlers Registration
def register_handlers_admin(dp : Dispatcher):
    dp.register_message_handler(cm_tokens_used, commands='tokens_used')
    dp.register_message_handler(cm_chats, commands='chats')
    dp.register_message_handler(cm_voice_records, commands='voice_records')
    dp.register_message_handler(moderator_command, commands=['moderator'], is_chat_admin=True)