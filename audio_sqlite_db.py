import sqlite3 as sq
from datetime import datetime
import pandas as pd 

dbase = sq.connect('elis_openai_plus.db')
cur = dbase.cursor()

def sql_start(logger) -> None:
    global dbase, cur
    
    if dbase:
        logger.warning("elis_openai_plus: Data base connected Ok!")
    dbase.execute('create table if not exists elis_openai_plus_use_log(use_date TEXT, user_name TEXT, user_id TEXT, action TEXT, words INT, language_code TEXT, confidence REAL)')
    dbase.commit()

def use_log_add_command(user_name, user_id, action, words, language_code, confidence):
    use_date = datetime.now()
    params = (use_date, user_name, user_id, action, words, language_code, confidence)
    dbase.execute('insert into elis_openai_plus_use_log values (?,?,?,?,?,?,?)', params)
    dbase.commit()

def sql_read() -> pd.DataFrame :
    
    df = pd.read_sql_query("SELECT * FROM elis_openai_plus_use_log", dbase)
    return df

