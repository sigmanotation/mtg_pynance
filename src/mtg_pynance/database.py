from mtg_pynance.config import Config
from mtg_pynance.database import retrieve_bulk_data
from mtg_pynance.collection import load_collection

from datetime import datetime
from pathlib import Path
import polars as pl
import numpy as np
import sqlite3
import json


def record_card_entry(bulk_data, collection, cid, timestamp, cursor):
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
        bulk_data.sql(f"select prices from self where id = '{id}'").item()[foilkey]
    )

    # Add card's purchase price to purchase_price table, if nonexistent
    sql_command = f"select count(*) from 'purchase_price' where cid = {cid}"
    cursor.execute(sql_command)
    rows = cursor.fetchone()[0]
    if rows == 0:
        sql_command = "insert into 'purchase_price' values (?, ?)"
        cursor.execute(sql_command, (cid, purchase_price))

    # Create card's table in dataframe, if nonexistent
    table_name = "card_" + str(cid)
    sql_command = f"create table if not exists {table_name} (timestamp STRING, market_value FLOAT)"
    cursor.execute(sql_command)

    # Insert card statistics into its table in database
    sql_command = f"insert into {table_name} VALUES (?, ?)"
    cursor.execute(
        sql_command,
        (timestamp, current_price),
    )


def make_collection_tables(bulk_data, collection, timestamp, cursor):
    """ """
    cid_array: np.ndarray = (
        collection.select(pl.col("cid")).collect().to_numpy().flatten()
    )
    for cid in cid_array:
        try:
            record_card_entry(bulk_data, collection, cid, timestamp, cursor)
        except:
            print(
                f"Could not calculate card statistics of card with collection ID {cid}!"
            )

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
    print("Workspace validated.")

    # Determine if local bulk data files exist and get their timestamp
    local_dt: datetime = config.get_bulk_data_timestamp()

    retrieve_bulk_data(
        config.get_bulk_info_path(), config.get_bulk_data_path(), local_dt
    )

    print("Importing collection and bulk data files...")
    collection: pl.LazyFrame = load_collection(config.collection_path)
    bulk_data: pl.DataFrame = pl.read_json(config.get_bulk_data_path())
    print("Collection and bulk data files imported.")

    # Connect to local SQL database, making it if it doesn't exist
    connection: sqlite3.Connection = sqlite3.connect(config.get_database_path())
    cursor: sqlite3.Cursor = connection.cursor()

    # Make table of purchase prices
    sql_command = (
        "create table if not exists 'purchase_price' (cid string, price float)"
    )
    cursor.execute(sql_command)

    make_collection_tables(bulk_data, collection, local_dt, cursor)
