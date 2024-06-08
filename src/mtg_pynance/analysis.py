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
    sql_command = "select cid from purchase_price"
    result = cursor.execute(sql_command).fetchall()

    mya = np.array([cid[0] for cid in result])
    # ppdict = {cid: price for cid, price in result}
    # result = cursor.execute(sql_command).fetchone()
    # for x in result:
    #     print(x)
    # connection.close()


def pull(database_path):
    # Connect to local SQL database
    connection: sqlite3.Connection = sqlite3.connect(database_path)
    cursor: sqlite3.Cursor = connection.cursor()

    # Calculate market value of all cards
    sql_command = "select * from card_0"
    result = cursor.execute(sql_command).fetchall()
    print(result)
