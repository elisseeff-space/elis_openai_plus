import sqlite3 as sq
#import logging
from datetime import datetime
import pandas as pd 
from create_bot import my_status

def sql_start() -> sq.Connection:
    #global my_status
    dbase = sq.connect('/home/pavel/github/elis_openai_plus/db/elis_openai_plus.db')
    cur = dbase.cursor()

    if dbase:
        my_status.logger.warning("elis_openai_plus: Data base connected Ok!")
    # log of voice recognition hystory
    dbase.execute('create table if not exists elis_openai_plus_use_log(use_date TEXT, user_name TEXT, user_id TEXT, action TEXT, words INT, language_code TEXT, confidence REAL)')
    # log of OpenAI chat hystory
    dbase.execute('create table if not exists elis_openai_log(message_date TEXT, user_id TEXT, user_name TEXT, chat_id TEXT, role TEXT, content TEXT, prompt_tokens INTEGER, completion_tokens INTEGER, total_tokens INTEGER)')
    dbase.execute('CREATE TABLE if not exists "config_param" ("param"  TEXT NOT NULL UNIQUE, "value"  TEXT, PRIMARY KEY("param"))')
    
    select_query = "SELECT value from config_param where param = 'help'"
    cur.execute(select_query)
    res = cur.fetchone()
    text = "Сейчас у Элис есть два режима работы с голосовыми сообщениями:\
Первый - это обычный диалог с ChatGPT, когда вы говорите фразу голосом, а Элис отвечает на нее, как если бы вы передали ее текстом.\
Второй - это дуэт с системой распознавания, когда Элис только исправляет текст, введенный голосом, являясь как бы редактором-корректором. \
При этом, есть три варианта корректировки текста: \
Первый - исправление текста (пропуски слов, орфография). \
Второй - это исправление текста в ласковом и нежном тоне, чтобы было приятно читать.\
Третий - это исправление текста с упором на медицинскую терминологию."
    if not res :
        params = ('help', text)
        insert_query = "insert into config_param values (?,?)"
        cur.execute(insert_query, params)
        dbase.commit()
    my_status.dbase = dbase

    dbase.commit()
    return dbase

def get_elis_chats_for_initialisation():
    #global my_status
    cur = my_status.dbase.cursor()
    select_query = "SELECT DISTINCT chat_id from elis_openai_log"
    cur.execute(select_query)
    res = cur.fetchall()
    if res is not None:
        return res
    else:
        my_status.logger.error("get_elis_chats_for_initialisation ERROR: SELECT DISTINCT chat_id from elis_openai_log!")

def get_chat_messages(chat_id):
    #global my_status
    cur = my_status.dbase.cursor()
    select_query = "SELECT role, content from elis_openai_log where chat_id = " + chat_id + " order by message_date LIMIT 5"
    cur.execute(select_query)
    res = cur.fetchall()
    if res is not None:
        return res
    else:
        my_status.logger.error("get_elis_chats_for_initialisation ERROR: SELECT DISTINCT chat_id from elis_openai_log!")

def get_help_text() -> str:
    #global my_status
    cur = my_status.dbase.cursor()
    select_query = "SELECT value from config_param where param = 'help'"
    cur.execute(select_query)
    res = cur.fetchone()
    if res is not None:
        return res[0]
    else:
        my_status.logger.error("get_help_text ERROR: SELECT value from config_param where param = 'help'!")

def get_elis_stat():
    #global my_status
    cur = my_status.dbase.cursor()
    select_query = "SELECT user_name, role, count(*), sum(total_tokens) from elis_openai_log group by user_name, role"
    cur.execute(select_query)
    res = cur.fetchall()
    if res is not None:
        return res
    else:
        my_status.logger.error("get_elis_stat ERROR: SELECT user_name, role, count(*), sum(total_tokens) from elis_openai_log group by user_name, role !")

def get_voice_messages_stat():
    #global my_status
    cur = my_status.dbase.cursor()
    select_query = "SELECT user_name, count(*), sum(words) from elis_openai_plus_use_log group by user_name"
    cur.execute(select_query)
    res = cur.fetchall()
    if res is not None:
        return res
    else:
        my_status.logger.error("get_voice_messages_stat ERROR: SELECT user_name, count(*), sum(words) from elis_openai_plus_use_log !")
         

def elis_openai_log_insert(message_date, user_id: str, user_name: str, chat_id: str, role: str,
                content: str, prompt_tokens: int, completion_tokens: int, total_tokens: int) -> bool :
    #global my_status
    #use_date = datetime.now()
    params = (message_date, user_id, user_name, chat_id, role, content, prompt_tokens, completion_tokens, total_tokens)
    my_status.dbase.execute('insert into elis_openai_log values (?,?,?,?,?,?,?,?,?)', params)
    my_status.dbase.commit()
    return True

def use_log_add_command(user_name, user_id, action, words, language_code, confidence) -> bool:
    #global my_status
    use_date = datetime.now()
    params = (use_date, user_name, user_id, action, words, language_code, confidence)
    my_status.dbase.execute('insert into elis_openai_plus_use_log values (?,?,?,?,?,?,?)', params)
    my_status.dbase.commit()
    return True
def sql_read_tokens() :
    #global my_status
    cur = my_status.dbase.cursor()
    select_query = "SELECT sum(prompt_tokens), sum(completion_tokens), sum(total_tokens) from elis_openai_log"
    cur.execute(select_query)
    res = cur.fetchone()
    #print(res)
    #print(type(res))
    return res

def sql_read(dbase: sq.Connection) -> pd.DataFrame :
    #global my_status
    df = pd.read_sql_query("SELECT * FROM elis_openai_plus_use_log", my_status.dbase)
    return df

