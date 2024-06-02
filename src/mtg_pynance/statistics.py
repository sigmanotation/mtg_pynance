from pathlib import Path
import polars as pl
import numpy as np


def collection_valid(collection: pl.LazyFrame):
    """
    Checks input collection file for compliance to prevent code breaking downstream.

    Parameters
    ----------
    """
    rows: int = collection.select(pl.count()).collect().item()

    # Check if every card has an ID
    if collection.select(pl.col("id")).count().collect().item() != rows:
        raise Exception("Some cards are missing ID's! Check collection file!")

    # Check if every card has a unique ID
    if collection.select(pl.col("id")).collect().unique(keep="any").height != rows:
        raise Exception("Not every card has a unique ID! Check collection file!")

    # Check if every card has an integer ID
    # Note that polars seems to default interpret ints as int64
    if not isinstance(collection.schema["id"], pl.Int64):
        raise Exception("ID's are not integers! Check collection file!")

    # Check if every card has a foil type
    if collection.select(pl.col("foil")).count().collect().item() != rows:
        raise Exception("Some cards are missing foil types! Check collection file!")

    # Check if foil types are of allowed kind
    if (
        collection.filter(pl.col("foil") != "none" & pl.col("foil") != "foil")
        .collect()
        .height
        != rows
    ):
        raise Exception("Some cards have invalid foil types! Check collection file!")


# def card_stats(bulk_data, collection, row):
#     """
#     Calculates card statistics and returns them in a Numpy 1x3 matrix. The 0th element is the card's
#     current price, the 1st element is the purchase price, and the 3rd element is the profit.

#     Calculates card statistics, which are its current price, purchase price, and profit.

#     Parameters
#     ----------
#     bulk_data: Path
#         Path to Scryfall's bulk data default cards json file.
#     collection: Path
#         Path to csv file of collection of cards.

#     Variables:
#        row: integer of row in collection dataframe corresponding to one card
#     """
#     # Use a try-except structure to capture a multitude of possible errors with collection and bulk data files
#     try:
#         # Get id and foil information of card in input row
#         id = collection.row(row, named=True)["id"]
#         foil = collection.row(row, named=True)["foil"]

#         # determine status of foil
#         foilkey = ""
#         if foil == "none":
#             foilkey = "usd"
#         elif foil == "foil":
#             foilkey = "usd_foil"
#         else:
#             foilkey = "usd_etched"

#         # determine current price, purchase price, and profit
#         c_price = float(
#             bulk.row(by_predicate=(pl.col("id") == id), named=True)["prices"][foilkey]
#         )
#         p_price = collection.row(row, named=True)["purchase_price"]
#         profit = c_price - p_price
#     except:
#         print(f"Error with card with collection_id {row}. Check CSV.")
#         return None

#     # Return results as NumPy array
#     matrix = np.array([c_price, p_price, profit])

#     return matrix


# def collection_stats(bulk, collection):
#     """
#     The main function of mtg pynance. It calculates the card statistics of every card in the collection with the
#     downloaded Scryfall default cards bulk data file and writes the statistics for each card to a table
#     in the created SQL database called "collection_statistics.db". The overall collection statistics are calculated
#     as well and written to a table in the same database. If a table in the database already has an entry with the
#     downloaded default cards file, nothing will be added to it.

#     Variables:
#         bulk, collection: Polars dataframes. bulk is the Scryfall dataframe and collection is the collection dataframe.
#     """
#     # Validate collection file
#     # do validation

#     # Connect to local SQL database
#     connection = sqlite3.connect("collection_statistics.db")
#     cursor = connection.cursor()

#     # Total number of cards in collection
#     cardcount = collection.select(pl.count()).item()

#     # Determine timestamp of default_cards file
#     dc_df = pl.read_json("bulk_data_info.json")
#     dc_ts = dc_df.row(0, named=True)["updated_at"]
#     dc_dt = datetime.fromisoformat(dc_ts)

#     # Calculate the profit and value of each card and add it to respective total
#     collection_matrix = np.zeros(3)
#     gain_loss_percent = 0

#     for card in range(cardcount):
#         # Create tablename of card
#         collection_id = collection.row(card, named=True)["collection_id"]
#         tablename = "card_" + str(collection_id)

#         # Calculate card statistics
#         card_matrix = card_stats(bulk, collection, card)
#         if card_matrix is None:
#             continue
#         gain_loss_percent = (card_matrix[0] - card_matrix[1]) / card_matrix[1] * 100

#         # Create card's table in dataframe, if nonexistent. Delete last tuple added to its table
#         # if its timestamp is the same as the currently downloaded default_cards file
#         db_table(cursor, tablename, dc_dt)

#         # Insert card statistics into its table in database
#         sql_command = """INSERT INTO {} VALUES (?, ?, ?, ?, ?)""".format(tablename)
#         cursor.execute(
#             sql_command,
#             (dc_ts, card_matrix[0], card_matrix[1], card_matrix[2], gain_loss_percent),
#         )

#         # Calculate collection statistics
#         collection_matrix += card_matrix
#         gain_loss_percent = (
#             (collection_matrix[0] - collection_matrix[1]) / collection_matrix[1] * 100
#         )

#     # Make table called "collection" in database if it does not exist and add collection statistics
#     db_table(cursor, "collection", dc_dt)
#     sql_command = """INSERT INTO {} VALUES (?, ?, ?, ?, ?)""".format("collection")
#     cursor.execute(
#         sql_command,
#         (
#             dc_ts,
#             collection_matrix[0],
#             collection_matrix[1],
#             collection_matrix[2],
#             gain_loss_percent,
#         ),
#     )

#     connection.commit()
#     connection.close()

#     return


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
