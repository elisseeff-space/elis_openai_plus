import json

from aiogram import Bot
#from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher
import sqlite3 as sq

file = open('/home/pavel/cfg/config.json', 'r')
config = json.load(file)

class BotStatus:
    rows_qty_to_select = 5
    #rows_offset = 0
    
    def __init__(self, lang, rows_offset, dbase: sq.Connection):
        self.lang = lang
        self.rows_offset = rows_offset
        self.dbase = dbase
    def set_language(self, lang):
        self.lang = lang
    def get_language(self) -> str:
        return self.lang
    def add_rows_selected(self, rows_offset: int):
        self.rows_offset += self.rows_offset
    def clear_rows_selected(self):
        self.rows_offset = 0
    def get_offset(self) -> int:
        return int(self.rows_offset)
    def get_qty_to_select(self) -> int:
        return int(self.rows_qty_to_select)
    
my_status = BotStatus('auto', 0, 0)

#bot = Bot(token = config['rtlab_voice_bot_token'])
bot = Bot(token = config['VoskModelSTT_bot'])

#dp = Dispatcher(bot, storage=storage)
dp = Dispatcher(bot)