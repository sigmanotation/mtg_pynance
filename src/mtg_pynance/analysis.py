from pathlib import Path
from datetime import datetime
import sqlite3
import numpy as np


def collection_value(database_path: Path):
    """ """
    # Connect to local SQL database
    connection: sqlite3.Connection = sqlite3.connect(database_path)
    cursor: sqlite3.Cursor = connection.cursor()

    # Calculate market value of all cards
    sql_command = "select * from purchase_price"
    result = cursor.execute(sql_command).fetchall()

    card_id_db = np.array([cid for cid in result])
    mydict = {}
    for cid, price in enumerate(card_id_db):
        sql_command = f"select * from card_{cid}"
        result = cursor.execute(sql_command).fetchall()
        combined = {key: mydict.get(key, 0) + new.get(key, 0) for key in set(old) | set(new)} 
        mydict = {asdfasdf for timestamp in set(mydict) | set}


    # connection.close()


def wee(cid, dicty):




def pull(database_path):
    # Connect to local SQL database
    connection: sqlite3.Connection = sqlite3.connect(database_path)
    cursor: sqlite3.Cursor = connection.cursor()

    # Calculate market value of all cards
    sql_command = "select * from card_0"
    result = cursor.execute(sql_command).fetchall()
    print(result)
