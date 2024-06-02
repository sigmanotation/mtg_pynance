from mtg_pynance.database import retrieve_database
from mtg_pynance.statistics import collection_valid
import polars as pl

# retrieve_database("/Users/zachserikow/Desktop/her")

lf = pl.LazyFrame(
    {"id": [1, 2, 3, 5], "foil": ["foil", "none", "etched", "none"], "c": [6, 8, 7, 7]}
)
# print(type(lf.collect()[3, 0]))

collection_valid(lf)
