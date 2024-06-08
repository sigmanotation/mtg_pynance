from pathlib import Path
from datetime import datetime
import sqlite3


def collection_value(database_path: Path):
    """ """
    # Connect to local SQL database
    connection: sqlite3.Connection = sqlite3.connect(database_path)
    cursor: sqlite3.Cursor = connection.cursor()

    # Calculate market value of all cards
    sql_command = "select * from purchase_price"
    result = cursor.execute(sql_command).fetchall()
    ppdict = {cid: price for cid, price in result}
    connection.close()
