import openai
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import json
from sqlite_db import elis_openai_log_insert, sql_start
from create_bot import bot, my_status

file = open('/home/pavel/cfg/config.json', 'r')
config = json.load(file)

openai.api_key = config['openai']

# storage = MemoryStorage()

def update(chat_id, group_messages, role, content, count_messages) -> bool:
    
    messages_int=[
    #{"role": "system", "content": "Technology, Medicine and Science consultant"},
    {"role": "system", "content": "Ты консультант по разным жизненным ситуациям. Тебя зовут Элис."},
    {"role": "user", "content": "Мы хотим узнать много нового и интересного."},
    {"role": "assistant", "content": "День добрый! Что бы вы хотели узнать?"}]

    # Check if the chat ID is already in the dictionary
    if chat_id not in group_messages:
        group_messages[chat_id] = messages_int
    else:
        group_messages[chat_id].append({"role": role, "content": content})

    if chat_id not in count_messages:
        count_messages[chat_id] = 0
    else: 
        count_messages[chat_id] += 1

    if(len(group_messages[chat_id])) > 11:
        group_messages[chat_id].pop(3)
    
    #elis_openai_log_insert(my_status.dbase, message.date, str(message.from_user.id), str(message.from_user.username), 'chat_user', str(message.text))

    return True

# Функция отправляет количество израсходованных токенов
# После запуска бота, пользователь может отправить команду `/token_count` и 
# получить количество токенов в ответном сообщении. 
# Обратите внимание, что в этом коде используется `await`, так как это асинхронный код.
async def get_token_count(message) -> bool:
    
    await bot.send_message(chat_id=message.chat.id, 
            text=f"Расход токенов при вводе сообщения в бот: <Coming soon :-)>")
    await bot.send_message(chat_id=message.chat.id, 
            text=f"Токенов расходуется на ответ API OpenAI при выводе сообщения в бот: <Coming soon :-)>")
    await bot.send_message(chat_id=message.chat.id, 
            text=f"Всего токенов израсходовано на запрос и на ответ (суммарно в задании к боту): <Coming soon :-)>")

    await bot.send_message(chat_id=message.chat.id, 
            text=f"Всего чатов обслуживается: {str(len(group_messages))}")
    for i in group_messages:
        await bot.send_message(chat_id=message.chat.id, 
            text=f"Всего обработано сообщений в чате {i}: {str(count_messages[i])}\nContest Bufer Size: {str(len(group_messages[i]))}")
    return True

def call_openai(chat_id) :
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages = my_status.group_messages[chat_id]
        )
    return response

async def send(message : types.Message):
    
    # Get the chat ID and user ID
    chat_id = str(message.chat.id)
    #chat_id = message.chat.id
    bot_info = await message.bot.get_me()
    try:
        if f'@{bot_info.username}' in message.text:
            await bot.send_chat_action(message.chat.id, 'typing')
            update(chat_id, my_status.group_messages, "user", message.text, my_status.count_messages)
            elis_openai_log_insert(my_status.dbase, message.date, str(message.from_user.id), 
                        str(message.from_user.username), 'chat_user', str(message.text), 0, 0, 0)
            chat_response = call_openai(chat_id)
            update(chat_id, my_status.group_messages, "assistant", chat_response['choices'][0]['message']['content'], my_status.count_messages)
            elis_openai_log_insert(my_status.dbase, message.date, str(message.from_user.id), 
                        str(message.from_user.username), 'assistant', chat_response['choices'][0]['message']['content'], 
                        int(chat_response['usage']['prompt_tokens']), int(chat_response['usage']['completion_tokens']), int(chat_response['usage']['total_tokens']))
            await message.answer(chat_response['choices'][0]['message']['content'])

    except openai.error.APIError as e:
        if e.status_code == 429:
            # Too many requests, wait and retry
            time.sleep(2 ** e.retry_after)
            return generate_text(prompt)
        else:
            # Other error, raise an exception
            raise Exception("OpenAI API error: {}".format(e.message))

if __name__ == '__main__':
    print('Hello!')
    #dbase = sql_start(logger)
    #cur = dbase.cursor()

