import sqlite3 as sq
from datetime import datetime
import pandas as pd 
from create_bot import my_status

def sql_start(logger) -> sq.Connection:
    
    dbase = sq.connect('/home/pavel/github/elis_openai_plus/db/elis_openai_plus.db')

    if dbase:
        logger.warning("elis_openai_plus: Data base connected Ok!")
    # log of voice recognition hystory
    dbase.execute('create table if not exists elis_openai_plus_use_log(use_date TEXT, user_name TEXT, user_id TEXT, action TEXT, words INT, language_code TEXT, confidence REAL)')
    # log of OpenAI chat hystory
    dbase.execute('create table if not exists elis_openai_log(message_date TEXT, user_id TEXT, user_name TEXT, role TEXT, content TEXT, prompt_tokens INTEGER, completion_tokens INTEGER, total_tokens INTEGER)')
    
    my_status.dbase = dbase

    dbase.commit()
    return dbase

def elis_openai_log_insert(dbase: sq.Connection, message_date, user_id: str, user_name: str, role: str,
                content: str, prompt_tokens: int, completion_tokens: int, total_tokens: int) -> bool :
    #use_date = datetime.now()
    params = (message_date, user_id, user_name, role, content, prompt_tokens, completion_tokens, total_tokens)
    dbase.execute('insert into elis_openai_log values (?,?,?,?,?,?,?,?)', params)
    dbase.commit()
    return True

def use_log_add_command(dbase: sq.Connection, user_name, user_id, action, words, language_code, confidence):
    use_date = datetime.now()
    params = (use_date, user_name, user_id, action, words, language_code, confidence)
    dbase.execute('insert into elis_openai_plus_use_log values (?,?,?,?,?,?,?)', params)
    dbase.commit()

def sql_read(dbase: sq.Connection) -> pd.DataFrame :
    
    df = pd.read_sql_query("SELECT * FROM elis_openai_plus_use_log", dbase)
    return df

