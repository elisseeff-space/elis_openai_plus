from sqlite_db import use_log_add_command
#from elis_google_stt import transcribe_file
from pathlib import Path
from aiogram import Dispatcher, types
from aiogram.types import ContentType, File, Message, ReplyKeyboardRemove
from create_bot import bot, my_status
from client_kb import kb_client
from recognize_yandex_stt import transcribe_file
from datetime import datetime
from elis_openai import send, get_token_count, update, call_openai, group_messages, count_messages

#@dp.message_handler(commands=['start', 'help'])
async def command_start(message : types.Message):
    try:
        await bot.send_message(message.from_user.id, 'Hi! It is Yandex voice recognition bot. You can send voice message.', reply_markup=kb_client)
        #await message.delete()
    except:
        await message.reply('Something wrong with me... \nhttps://t.me/rtlab_voice_bot', reply_markup=kb_client)

async def handle_file(file: File, file_name: str, path: str):
    Path(f"{path}").mkdir(parents=True, exist_ok=True)

    await bot.download_file(file_path=file.file_path, destination=f"{path}/{file_name}")

# @dp.message_handler(content_types=[ContentType.VOICE])
async def voice_message_handler(message: Message): # types.Message):
    # Get the file ID of the voice message
    voice = await message.voice.get_file()
    path = "/home/pavel/github/elis_openai_plus/voices"

    await handle_file(file=voice, file_name=f"{voice.file_id}.ogg", path=path)
    
    file_name = path + f"/{voice.file_id}.ogg"
    start_time = datetime.now()
    str_buf = f"Recognition starts at: {start_time.strftime('%H:%M:%S')}."
    await message.answer(str_buf)
    alternative = transcribe_file(file_name)
    end_time = datetime.now()
    runtime = end_time - start_time
    str_buf = f"Recognition ready in: {runtime.seconds} seconds. Elis starts some corrections."
    start_time = end_time
    await message.answer(str_buf)

    str_buf = 'исправь текст: ' + alternative.text
    update(88888, group_messages, "user", str_buf, count_messages)
    chat_response = call_openai(88888)
    update(88888, group_messages, "assistant", chat_response, count_messages)
    end_time = datetime.now()
    runtime = end_time - start_time
    str_buf = f"Elis ready in: {runtime.seconds} seconds."
    await message.answer(str_buf)

    use_log_add_command(my_status.dbase, message.from_user.username, message.from_user.id, alternative.text, len(alternative.words), my_status.get_language(), float(alternative.confidence))
    await message.answer(chat_response)

async def language_ru_command(message : types.Message):
    my_status.set_language('ru-RU')
    #await bot.send_message(message.from_user.id, 'Russian Language of Voice Messages.')
    await message.reply('Russian Language of Voice Messages.')

async def language_en_command(message : types.Message):
    my_status.set_language('en-US')
    #await bot.send_message(message.from_user.id, 'English Language of Voice Messages.')
    await message.reply('English Language of Voice Messages.')

async def language_fr_command(message : types.Message):
    my_status.set_language('fr-FR')
    #await bot.send_message(message.from_user.id, 'France Language of Voice Messages.')
    await message.reply('France Language of Voice Messages.')

async def language_de_command(message : types.Message):
    my_status.set_language('de-DE')
    #await bot.send_message(message.from_user.id, 'France Language of Voice Messages.')
    await message.reply('German Language of Voice Messages.')

async def language_auto_command(message : types.Message):
    my_status.set_language('auto')
    #await bot.send_message(message.from_user.id, 'France Language of Voice Messages.')
    await message.reply('автоматическое распознавание языка.')

def register_handlers_client(dp : Dispatcher):

    # OpenAI handlers
    dp.register_message_handler(get_token_count, commands=['token_count'])

    # Voice recognition handlers
    dp.register_message_handler(voice_message_handler, content_types=[
    types.ContentType.VOICE,
    types.ContentType.AUDIO,
    types.ContentType.DOCUMENT
    ])
    dp.register_message_handler(command_start, commands=['start', 'help'])
    dp.register_message_handler(language_ru_command, commands=['ru'])
    dp.register_message_handler(language_en_command, commands=['en'])
    dp.register_message_handler(language_fr_command, commands=['fr'])
    dp.register_message_handler(language_auto_command, commands=['auto'])
    dp.register_message_handler(language_de_command, commands=['de'])

    dp.register_message_handler(send)