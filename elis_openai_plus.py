import logging
from aiogram.utils import executor
from sqlite_db import sql_start
from admin import register_handlers_admin
from client import register_handlers_client
from other import register_handlers_other
from create_bot import dp, my_status

#from datetime import datetime

register_handlers_client(dp)
register_handlers_admin(dp)
register_handlers_other(dp)

my_status.logger = logging.getLogger(__name__)
#formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
logging.basicConfig(
    level=logging.INFO,
    filename="/home/pavel/github/elis_openai_plus/log/elis_openai_plus_bot.log",
    format='%(asctime)s - %(levelname)s - %(message)s'
)

async def on_startup(_):
    my_status.logger.warning("Elisseeff Elis_OpenAI_plus Bot logging is ON!")
    
# Start the bot
if __name__ == '__main__':
    sql_start()
    try:
        executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
    except (KeyboardInterrupt, SystemExit):
        pass