from pathlib import Path
import sqlite3
import polars as pl


def collection_stats(database_path: Path):
    """
    Calculates the market value and gain/loss of the entire collection of cards
    in the local SQL database at the timestamps the prices were recorded.

    Parameters
    ----------
    database_path: Path
        Path to the local SQL collection database.

    Returns
    -------
    pl.DataFrame
        Returns dataframe with schema {"timestamp": pl.String,
        "market_value": pl.Float64, "profit": pl.Float64}.
    """
    # Connect to local SQL database
    connection: sqlite3.Connection = sqlite3.connect(database_path)
    cursor: sqlite3.Cursor = connection.cursor()

    # Get list of all cards
    sql_command = "select * from purchase_price"
    card_id_db = cursor.execute(sql_command).fetchall()
    collection_stats: list[list[str, float, float]] = []

    # Record stats for each card in the local database
    for _, (cid, purchase_price) in enumerate(card_id_db):
        sql_command = f"select * from card_{cid}"
        result = cursor.execute(sql_command).fetchall()
        card_stats = [
            [timestamp, value, value - purchase_price] for timestamp, value in result
        ]
        collection_stats.extend(card_stats)

    connection.close()

    # Convert stats from list of lists to dataframe
    df = pl.DataFrame(
        collection_stats,
        schema={
            "timestamp": pl.String,
            "market_value": pl.Float64,
            "gain/loss": pl.Float64,
        },
        orient="row",
    )

    # Add together cards that have the same timestamp
    df = df.group_by("timestamp").agg(
        pl.col("market_value").sum(), pl.col("gain/loss").sum()
    )

    # TODO ensure that this will always sort correctly because the timestampsa are strings
    # Sort dataframe from earliest to latest timestamps
    df = df.sort("timestamp")

    return df


def collection_extrema(database_path: Path):
    """
    Calculates the cards in the collection that currently have the largest gain
    and loss.

    Parameters
    ----------
    database_path: Path
        Path to the local SQL collection database.

    Returns
    -------
    tuple(dict[], dict[])
        Return a tuple of dictionaries where element 0 corresponds to the card
        with the maximum gain and element 1 corresponds to the card with the
        maximum loss. The schema for each dictionary is {"cid": [int], "*": float,
        "purchase_price": float} where * is "gain" or "loss", respectively.

    """
    # Connect to local SQL database
    connection: sqlite3.Connection = sqlite3.connect(database_path)
    cursor: sqlite3.Cursor = connection.cursor()

    # Get list of all cards
    sql_command = "select * from purchase_price"
    card_id_db = cursor.execute(sql_command).fetchall()

    gain = {"cid": [], "gain": 0.0, "purchase_price": 0.0}
    loss = {"cid": [], "loss": 0.0, "purchase_price": 0.0}

    for _, (cid, purchase_price) in enumerate(card_id_db):
        sql_command = f"select market_value from card_{cid} where timestamp=(select max(timestamp) from card_{cid})"
        current_price = cursor.execute(sql_command).fetchone()[0]
        # Calculate gain/loss of each card with respect to current price
        gain_loss = round(current_price - purchase_price, 2)

        # Record card's gain/loss if it is an extreme
        if gain_loss == gain["gain"]:
            gain["cid"].append(cid)

        if gain_loss > gain["gain"]:
            gain["cid"].clear()
            gain["cid"].append(cid)
            gain["gain"] = gain_loss
            gain["purchase_price"] = purchase_price

        if gain_loss == loss["loss"]:
            loss["cid"].append(cid)

        if gain_loss < loss["loss"]:
            loss["cid"].clear()
            loss["cid"].append(cid)
            loss["loss"] = gain_loss
            loss["purchase_price"] = purchase_price

    connection.close()

    return gain, loss


def collection_largest_movers(database_path: Path):
    """ """
    # Connect to local SQL database
    connection: sqlite3.Connection = sqlite3.connect(database_path)
    cursor: sqlite3.Cursor = connection.cursor()

    # Get list of all cards
    sql_command = "select * from purchase_price"
    card_id_db = cursor.execute(sql_command).fetchall()

    gain = {"cid": [], "gain": 0.0, "purchase_price": 0.0}
    loss = {"cid": [], "loss": 0.0, "purchase_price": 0.0}

    for _, (cid, purchase_price) in enumerate(card_id_db):
        sql_command = f"""select market_value - lag(market_value) over (order by timestamp) 
                          from card_{cid} order by timestamp desc limit 1"""
        result = cursor.execute(sql_command).fetchone()[0]

        if result is None:
            continue

        movement = round(result, 2)

        # Record card's gain/loss if it is an extreme
        if movement == gain["gain"]:
            gain["cid"].append(cid)

        if movement > gain["gain"]:
            gain["cid"].clear()
            gain["cid"].append(cid)
            gain["gain"] = movement
            gain["purchase_price"] = purchase_price

        if movement == loss["loss"]:
            loss["cid"].append(cid)

        if movement < loss["loss"]:
            loss["cid"].clear()
            loss["cid"].append(cid)
            loss["loss"] = movement
            loss["purchase_price"] = purchase_price

    connection.close()

    return gain, loss


def pull(database_path):
    # Connect to local SQL database
    connection: sqlite3.Connection = sqlite3.connect(database_path)
    cursor: sqlite3.Cursor = connection.cursor()

    # # Calculate market value of all cards
    # sql_command = "select * from card_0"
    # result = cursor.execute(sql_command).fetchall()

    sql_command = "select * from purchase_price"
    card_id_db = cursor.execute(sql_command).fetchall()
    for x in card_id_db:
        print(x)
    print(len(card_id_db))

    # print(result)


def delete(database_path):
    # Connect to local SQL database
    connection: sqlite3.Connection = sqlite3.connect(database_path)
    cursor: sqlite3.Cursor = connection.cursor()

    sql_command = """DROP TABLE purchase_price"""
    cursor.execute(sql_command)
    connection.close()
