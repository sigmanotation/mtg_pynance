from mtg_pynance.config import Config
from mtg_pynance.database import retrieve_bulk_data
from mtg_pynance.collection import load_collection

from datetime import datetime
from pathlib import Path
import polars as pl
import numpy as np
import sqlite3
import json


def do_card_stats(bulk_data, collection, cid, timestamp, cursor):
    """
    Calculates card statistics and returns them in a Numpy 1x3 matrix. The 0th element is the card's
    current price, the 1st element is the purchase price, and the 3rd element is the profit.

    Calculates card statistics, which are its current price, purchase price, and profit.

    Parameters
    ----------
    bulk_data: Path
        Path to Scryfall's bulk data default cards json file.
    collection: Path
        Path to csv file of collection of cards.
    cid: int
        cid of card in collection file.
    cursor:
    """
    # Card info from collection file
    id: str = collection.filter(pl.col("cid") == cid).collect().select("id").item()
    foiling: str = (
        collection.filter(pl.col("cid") == cid).collect().select("foiling").item()
    )
    purchase_price: float = (
        collection.filter(pl.col("cid") == cid)
        .collect()
        .select("purchase_price")
        .item()
    )

    # Card's foil status
    if foiling == "none":
        foilkey = "usd"
    elif foiling == "foil":
        foilkey = "usd_foil"
    else:
        foilkey = "usd_etched"

    # TODO SQL seems to be slightly faster, should check more
    # a = bulk_data.row(by_predicate=(pl.col("id") == id), named=True)["prices"][foilkey]

    # Card's current price from bulk data file
    current_price = float(
        bulk_data.sql(f"SELECT prices FROM self WHERE  id = '{id}'").item()[foilkey]
    )

    profit = current_price - purchase_price

    matrix = np.array([current_price, purchase_price, profit])

    # # Create card's table in dataframe, if nonexistent. Delete last tuple added to its table
    # # if its timestamp is the same as the currently downloaded default_cards file
    # table_name = str(cid)
    # db_table(cursor, table_name, dc_dt)

    # # Insert card statistics into its table in database
    # sql_command = f"""INSERT INTO {table_name} VALUES (?, ?, ?, ?, ?)"""
    # cursor.execute(
    #     sql_command,
    #     (dc_ts, card_matrix[0], card_matrix[1], card_matrix[2], gain_loss_percent),
    # )

    return matrix


def do_collection_stats(bulk_data, collection, timestamp, cursor):
    """ """
    # Calculate the profit and value of each card and add it to respective total
    collection_matrix = np.zeros(3)
    gain_loss_percent = 0

    cid_array: np.ndarray = (
        collection.select(pl.col("cid")).collect().to_numpy().flatten()
    )
    for card in cid_array:
        # SQL tablename of card
        table_name = str(card)

        # Calculate card statistics
        try:
            card_matrix = do_card_stats(bulk_data, collection, card, cursor, timestamp)
        except:
            print(
                f"Could not calculate card statistics of card with collection ID {card}!"
            )

    # gain_loss_percent = (card_matrix[0] - card_matrix[1]) / card_matrix[1] * 100

    #     # Create card's table in dataframe, if nonexistent. Delete last tuple added to its table
    #     # if its timestamp is the same as the currently downloaded default_cards file
    #     db_table(cursor, tablename, dc_dt)

    #     # Insert card statistics into its table in database
    #     sql_command = """INSERT INTO {} VALUES (?, ?, ?, ?, ?)""".format(tablename)
    #     cursor.execute(
    #         sql_command,
    #         (dc_ts, card_matrix[0], card_matrix[1], card_matrix[2], gain_loss_percent),
    #     )

    #     # Calculate collection statistics
    #     collection_matrix += card_matrix
    #     gain_loss_percent = (
    #         (collection_matrix[0] - collection_matrix[1]) / collection_matrix[1] * 100
    #     )

    # # Make table called "collection" in database if it does not exist and add collection statistics
    # db_table(cursor, "collection", dc_dt)
    # sql_command = """INSERT INTO {} VALUES (?, ?, ?, ?, ?)""".format("collection")
    # cursor.execute(
    #     sql_command,
    #     (
    #         dc_ts,
    #         collection_matrix[0],
    #         collection_matrix[1],
    #         collection_matrix[2],
    #         gain_loss_percent,
    #     ),
    # )

    # connection.commit()
    # connection.close()


def db_table(cursor, tablename, timestamp):
    """
    Creates a table in the database of the input cursor if it does not exist and returns true. If it does exist,
    the function determines whether the table's most recent entry was calculated using the currently
    downloaded Scryfall default cards bulk data file. If it was, false is returned, otherwise true is.
    The format of the created table is: (timestamp STRING, market_value FLOAT, cost_basis FLOAT,
    gain_loss FLOAT, gain_loss_percent FLOAT).

    Variables:
        cursor: SQLite3 object that is connected to a database
        tablename: string for the table's name in the database
        timestamp: datetime object that is the timestamp of the currently downloaded default cards file
    """
    # Determine if database exists
    sql_command = (
        """SELECT name FROM sqlite_master WHERE type='table' AND name='{}'""".format(
            tablename
        )
    )
    cursor.execute(sql_command)

    # Database does not exists, so make it
    if cursor.fetchone() is None:

        sql_command = """create table if not exists {} (timestamp STRING, market_value FLOAT, cost_basis FLOAT,
        gain_loss FLOAT, gain_loss_percent FLOAT)""".format(
            tablename
        )
        cursor.execute(sql_command)

    # Database does exist, determine when it was last updated
    else:

        # Query the timestamp of the last added tuple to the table
        sql_command = """SELECT * FROM {} ORDER BY timestamp DESC LIMIT 1""".format(
            tablename
        )
        cursor.execute(sql_command)
        result = cursor.fetchone()
        last_dt = datetime.fromisoformat(result[0])

        # If the timestamp of the downloaded default_cards file is the same as the timestamp
        # of the last tuple added to the table exit, delete the last added tuple
        if timestamp == last_dt:

            sql_command = """DELETE FROM {} WHERE timestamp = (SELECT MAX(timestamp) FROM {})""".format(
                tablename, tablename
            )
            cursor.execute(sql_command)


def run_mtg_pynance(config: Config):
    """
    The main function of mtg pynance. It calculates the card statistics of every card in the collection with the
    downloaded Scryfall default cards bulk data file and writes the statistics for each card to a table
    in the created SQL database called "collection_statistics.db". The overall collection statistics are calculated
    as well and written to a table in the same database. If a table in the database already has an entry with the
    downloaded default cards file, nothing will be added to it.

    Variables:
        bulk, collection: Polars dataframes. bulk is the Scryfall dataframe and collection is the collection dataframe.
    """
    config.create_workspace()
    print("Workspace made.")

    # Determine if local bulk data files exist and get their timestamp
    local_dt: datetime = config.get_bulk_data_timestamp()

    retrieve_bulk_data(
        config.get_bulk_info_path(), config.get_bulk_data_path(), local_dt
    )

    return

    collection: pl.LazyFrame = load_collection(config.collection_path)
    bulk_data: pl.DataFrame = pl.read_json(config.get_bulk_data_path())
    print("Collection and bulk data files imported.")

    # Connect to local SQL database
    connection: sqlite3.Connection = sqlite3.connect(config.get_database_path())
    cursor: sqlite3.Cursor = connection.cursor()

    do_collection_stats(bulk_data, collection, local_dt, cursor)
