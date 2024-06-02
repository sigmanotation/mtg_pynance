from mtg_pynance.config import Config
from mtg_pynance.collection import load_collection

from datetime import datetime
from pathlib import Path
import polars as pl
import numpy as np
import sqlite3


def do_card_stats(bulk_data, collection, cid):
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

    Variables:
       row: integer of row in collection dataframe corresponding to one card
    """
    id = collection.filter(pl.col("cid") == cid).collect().select("id").item()
    foiling = collection.filter(pl.col("cid") == cid).collect().select("foiling").item()
    print(id)
    print(foiling)

    # # determine status of foil
    # foilkey = ""
    # if foil == "none":
    #     foilkey = "usd"
    # elif foil == "foil":
    #     foilkey = "usd_foil"
    # else:
    #     foilkey = "usd_etched"

    print(bulk_data.filter(pl.col("id") == id).collect())
    # # determine current price, purchase price, and profit
    # c_price = float(
    #     bulk.row(by_predicate=(pl.col("id") == id), named=True)["prices"][foilkey]
    # )
    # p_price = collection.row(row, named=True)["purchase_price"]
    # profit = c_price - p_price

    # # Return results as NumPy array
    # matrix = np.array([c_price, p_price, profit])

    # return matrix


def do_collection_stats(config: Config):
    """
    The main function of mtg pynance. It calculates the card statistics of every card in the collection with the
    downloaded Scryfall default cards bulk data file and writes the statistics for each card to a table
    in the created SQL database called "collection_statistics.db". The overall collection statistics are calculated
    as well and written to a table in the same database. If a table in the database already has an entry with the
    downloaded default cards file, nothing will be added to it.

    Variables:
        bulk, collection: Polars dataframes. bulk is the Scryfall dataframe and collection is the collection dataframe.
    """

    collection: pl.LazyFrame = load_collection(config.collection_path)
    bulk_data: pl.LazyFrame = pl.scan_csv(config.get_bulk_data_path())

    # Connect to local SQL database
    connection = sqlite3.connect("collection_statistics.db")
    cursor = connection.cursor()

    # # # Determine timestamp of default_cards file
    # # dc_df = pl.read_json("bulk_data_info.json")
    # # dc_ts = dc_df.row(0, named=True)["updated_at"]
    # # dc_dt = datetime.fromisoformat(dc_ts)

    # # Calculate the profit and value of each card and add it to respective total
    # collection_matrix = np.zeros(3)
    # gain_loss_percent = 0

    cid_array: np.ndarray = (
        collection.select(pl.col("cid")).collect().to_numpy().flatten()
    )
    for card in cid_array:
        # SQL tablename of card
        table_name = str(card)

        # Calculate card statistics
        try:
            card_matrix = do_card_stats(bulk_data, collection, card)
        except:
            print(
                f"Could not calculate card statistics of card with collection ID {card}!"
            )
        break

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

    return


# def db_table(cursor, tablename, timestamp):
#     """
#     Creates a table in the database of the input cursor if it does not exist and returns true. If it does exist,
#     the function determines whether the table's most recent entry was calculated using the currently
#     downloaded Scryfall default cards bulk data file. If it was, false is returned, otherwise true is.
#     The format of the created table is: (timestamp STRING, market_value FLOAT, cost_basis FLOAT,
#     gain_loss FLOAT, gain_loss_percent FLOAT).

#     Variables:
#         cursor: SQLite3 object that is connected to a database
#         tablename: string for the table's name in the database
#         timestamp: datetime object that is the timestamp of the currently downloaded default cards file
#     """
#     # Determine if database exists
#     sql_command = (
#         """SELECT name FROM sqlite_master WHERE type='table' AND name='{}'""".format(
#             tablename
#         )
#     )
#     cursor.execute(sql_command)

#     # Database does not exists, so make it
#     if cursor.fetchone() is None:

#         sql_command = """create table if not exists {} (timestamp STRING, market_value FLOAT, cost_basis FLOAT,
#         gain_loss FLOAT, gain_loss_percent FLOAT)""".format(
#             tablename
#         )
#         cursor.execute(sql_command)

#     # Database does exist, determine when it was last updated
#     else:

#         # Query the timestamp of the last added tuple to the table
#         sql_command = """SELECT * FROM {} ORDER BY timestamp DESC LIMIT 1""".format(
#             tablename
#         )
#         cursor.execute(sql_command)
#         result = cursor.fetchone()
#         last_dt = datetime.fromisoformat(result[0])

#         # If the timestamp of the downloaded default_cards file is the same as the timestamp
#         # of the last tuple added to the table exit, delete the last added tuple
#         if timestamp == last_dt:

#             sql_command = """DELETE FROM {} WHERE timestamp = (SELECT MAX(timestamp) FROM {})""".format(
#                 tablename, tablename
#             )
#             cursor.execute(sql_command)
