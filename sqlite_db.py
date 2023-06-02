import sqlite3 as sq
import logging
from datetime import datetime
import pandas as pd 
from create_bot import my_status

def sql_start() -> sq.Connection:
    
    dbase = sq.connect('/home/pavel/github/elis_openai_plus/db/elis_openai_plus.db')
    cur = dbase.cursor()

    if dbase:
        my_status.logger.warning("elis_openai_plus: Data base connected Ok!")
    # log of voice recognition hystory
    dbase.execute('create table if not exists elis_openai_plus_use_log(use_date TEXT, user_name TEXT, user_id TEXT, action TEXT, words INT, language_code TEXT, confidence REAL)')
    # log of OpenAI chat hystory
    dbase.execute('create table if not exists elis_openai_log(message_date TEXT, user_id TEXT, user_name TEXT, role TEXT, content TEXT, prompt_tokens INTEGER, completion_tokens INTEGER, total_tokens INTEGER)')
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

def get_help_text(dbase: sq.Connection, logger: logging.Logger) -> str:
    cur = dbase.cursor()
    select_query = "SELECT value from config_param where param = 'help'"
    cur.execute(select_query)
    res = cur.fetchone()
    if res is not None:
        return res[0]
    else:
        logger.error("get_help_text: ERROR SELECT value from config_param where param = 'help'!")
         

def elis_openai_log_insert(dbase: sq.Connection, message_date, user_id: str, user_name: str, role: str,
                content: str, prompt_tokens: int, completion_tokens: int, total_tokens: int) -> bool :
    #use_date = datetime.now()
    params = (message_date, user_id, user_name, role, content, prompt_tokens, completion_tokens, total_tokens)
    dbase.execute('insert into elis_openai_log values (?,?,?,?,?,?,?,?)', params)
    dbase.commit()
    return True

def use_log_add_command(dbase: sq.Connection, user_name, user_id, action, words, language_code, confidence) -> bool:
    use_date = datetime.now()
    params = (use_date, user_name, user_id, action, words, language_code, confidence)
    dbase.execute('insert into elis_openai_plus_use_log values (?,?,?,?,?,?,?)', params)
    dbase.commit()
    return True
def sql_read_tokens() :
    
    cur = my_status.dbase.cursor()
    select_query = "SELECT sum(prompt_tokens), sum(completion_tokens), sum(total_tokens) from elis_openai_log"
    cur.execute(select_query)
    res = cur.fetchone()
    print(res)
    print(type(res))
    return res

def sql_read(dbase: sq.Connection) -> pd.DataFrame :
    
    df = pd.read_sql_query("SELECT * FROM elis_openai_plus_use_log", dbase)
    return df

