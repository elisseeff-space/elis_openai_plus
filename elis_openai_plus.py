import logging
from aiogram.utils import executor
from sqlite_db import sql_start, get_elis_chats_for_initialisation, get_chat_messages
from admin import register_handlers_admin
from client import register_handlers_client
from other import register_handlers_other
from create_bot import dp, my_status
from openai_req import update

#from datetime import datetime

register_handlers_admin(dp)
#register_handlers_other(dp)
register_handlers_client(dp)

#my_status = BotStatus()
my_status.logger = logging.getLogger(__name__)
#formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
logging.basicConfig(
    level=logging.INFO,
    filename="/home/pavel/github/elis_openai_plus/log/elis_openai_plus_bot.log",
    format='%(asctime)s - %(levelname)s - %(message)s'
)

async def on_startup(_):
    my_status.logger.warning("Elisseeff Elis_OpenAI_plus Bot logging is ON!")
    my_status.dbase = sql_start()
    res = get_elis_chats_for_initialisation()
    for i in res:
        if i[0] is not None:
            res1 = get_chat_messages(i[0])
            for j in res1:
                update(i[0], my_status.group_messages, j[0], j[1], my_status.count_messages)
                print('chat id : ', j)
    
# Start the bot
if __name__ == '__main__':
    
    try:
        executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
    except (KeyboardInterrupt, SystemExit):
        pass