from pathlib import Path
import sqlite3
import polars as pl


def collection_stats(database_path: Path):
    """
    Calculates the market value and profit of the entire collection of cards
    in the local SQL database at the timestamps that the prices were recorded.

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
    )

    # Add together cards that have the same timestamp
    df = df.group_by("timestamp").agg(
        pl.col("market_value").sum(), pl.col("profit").sum()
    )

    return df


def pull(database_path):
    # Connect to local SQL database
    connection: sqlite3.Connection = sqlite3.connect(database_path)
    cursor: sqlite3.Cursor = connection.cursor()

    # Calculate market value of all cards
    sql_command = "select * from card_574"
    result = cursor.execute(sql_command).fetchall()
    print(result)
