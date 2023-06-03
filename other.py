from aiogram import types, Dispatcher
import json, string
from create_bot import dp#, bot

#@dp.message_handler()
async def echo_send(message : types.Message):
    #await message.answer(message.text)
    #await message.reply(message.text)
    #await bot.send_message(message.from_user.id, message.text)

    with open('/home/pavel/cfg/words.json', 'r', encoding='utf-8') as ffile:
        data = json.load(ffile)

    if {i.lower().translate(str.maketrans('', '', string.punctuation)) for i in message.text.split(' ')}\
        .intersection(set(i['word'] for i in data)) != set():
        await message.reply('Маты запрещены!')
        await message.delete()
    #else:
    #    await message.reply('I`m here.')

def register_handlers_other(dp : Dispatcher):
    dp.register_message_handler(echo_send)
