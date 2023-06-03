import json
import logging
from aiogram import Bot
#from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher
import sqlite3 as sq
#from sqlite_db import sql_start, get_elis_chats_for_initialisation, get_chat_messages

file = open('/home/pavel/cfg/config.json', 'r')
config = json.load(file)

class BotStatus:
    dbase: sq.Connection
    # Initialize a dictionary to store messages for each group
    # Здесь храним отдельные очереди сообщений для каждого группового чата,
    # из которого приходят сообщения
    group_messages = {}
    count_messages = {}
    open_ai_prefix = {}
    logger: logging.Logger

    #def __init__(self): 
        
        # Request prefix for message to OpenAi API request
        #self.open_ai_prefix[chat_id] = prefix
        
    def set_open_ai_prefix(self, chat_id: str, prefix: str):
        if prefix == '~~~':
            if chat_id not in self.open_ai_prefix.keys():
                self.open_ai_prefix[chat_id] = ''
        else: self.open_ai_prefix[chat_id] = prefix
    def get_open_ai_prefix(self, chat_id) -> str:
        return self.open_ai_prefix[chat_id]
    
    
my_status = BotStatus()

#bot = Bot(token = config['Elis_OpenAI_bot'])
bot = Bot(token = config['VoskModelSTT_bot'])

#dp = Dispatcher(bot, storage=storage)
dp = Dispatcher(bot)