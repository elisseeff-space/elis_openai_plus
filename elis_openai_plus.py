import json
import logging

from aiogram.utils import executor

import admin
from sqlite_db import sql_start
import client
import other
from create_bot import dp

#from datetime import datetime

client.register_handlers_client(dp)
admin.register_handlers_admin(dp)
other.register_handlers_other(dp)

logger = logging.getLogger(__name__)
#formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
logging.basicConfig(
    level=logging.INFO,
    filename="/home/pavel/github/elis_openai_plus/log/elis_openai_plus_bot.log",
    format='%(asctime)s - %(levelname)s - %(message)s'
)


file = open('/home/pavel/cfg/config.json', 'r')
config = json.load(file)
#rtlab_voice_bot_token

#now = datetime.now()

async def on_startup(_):
    logger.warning("Elisseeff Elis_OpenAI_plus Bot logging is ON!")
    
# Start the bot
if __name__ == '__main__':
    sql_start(logger)
    try:
        executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
    except (KeyboardInterrupt, SystemExit):
        pass