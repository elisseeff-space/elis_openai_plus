import openai
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import json

file = open('/home/pavel/cfg/config.json', 'r')
config = json.load(file)

openai.api_key = config['openai']

# storage = MemoryStorage()

def update(chat_id, group_messages, role, content, count_messages):
    
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

    if(len(group_messages[chat_id])) > 15:
        group_messages[chat_id].pop(3)
    
    return group_messages

# Initialize a dictionary to store messages for each group
# Здесь храним отдельные очереди сообщений для каждого группового чата,
# из которого приходят сообщения
group_messages = {}
count_messages = {}

# Global variables for Tokens counting
prompt_tokens = 0
completion_tokens = 0
total_tokens = 0

# Функция отправляет количество израсходованных токенов
# После запуска бота, пользователь может отправить команду `/token_count` и 
# получить количество токенов в ответном сообщении. 
# Обратите внимание, что в этом коде используется `await`, так как это асинхронный код.
async def get_token_count(message):
    
    await bot.send_message(chat_id=message.chat.id, 
            text=f"Расход токенов при вводе сообщения в бот: {str(prompt_tokens)}")
    await bot.send_message(chat_id=message.chat.id, 
            text=f"Токенов расходуется на ответ API OpenAI при выводе сообщения в бот: {str(completion_tokens)}")
    await bot.send_message(chat_id=message.chat.id, 
            text=f"Всего токенов израсходовано на запрос и на ответ (суммарно в задании к боту): {str(total_tokens)}")

    await bot.send_message(chat_id=message.chat.id, 
            text=f"Всего чатов обслуживается: {str(len(group_messages))}")
    for i in group_messages:
        await bot.send_message(chat_id=message.chat.id, 
            text=f"Всего обработано сообщений в чате {i}: {str(count_messages[i])}\nContest Bufer Size: {str(len(group_messages[i]))}")


dp.register_message_handler(get_token_count, commands=['token_count'])

@dp.message_handler()
async def send(message : types.Message):

    ff = open('workfile', 'a', encoding="utf-8")
    ff.write(str(message.date) + ', ' + str(message.from_user.username) + ', ' + str(message.text) +
'\n')
    ff.close()

    # Get the chat ID and user ID
    chat_id = str(message.chat.id)
    # user_id = str(message.from_user.id)

    bot_info = await message.bot.get_me()
    try:
        if f'@{bot_info.username}' in message.text:

            update(chat_id, group_messages, "user", message.text, count_messages)
            response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages = group_messages[chat_id]
            )
            #global token_count
            #global metadata
            global prompt_tokens
            prompt_tokens = prompt_tokens + int(response['usage']['prompt_tokens'])
            global completion_tokens
            completion_tokens = completion_tokens + int(response['usage']['completion_tokens'])
            global total_tokens
            total_tokens = total_tokens + int(response['usage']['total_tokens'])

            chat_response = response['choices'][0]['message']['content']
            update(chat_id, group_messages, "assistant", chat_response, count_messages)
            await message.answer(chat_response)

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
