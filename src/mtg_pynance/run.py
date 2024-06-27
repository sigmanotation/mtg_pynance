from mtg_pynance.config import Config
from mtg_pynance.database import run_mtg_pynance
from mtg_pynance.analysis import (
    collection_stats,
    pull,
    delete,
    collection_extrema,
)
from pathlib import Path
import time

start_time = time.time()

workspace_path = Path("/Users/zachserikow/Desktop/pus")
collection_path = Path("/Users/zachserikow/Desktop/collection.csv")

config = Config(workspace_path, collection_path)

# run_mtg_pynance(config)

# ab = collection_stats(config.get_database_path())
# print(ab)

print(collection_extrema(config.get_database_path()))

# pull(config.get_database_path())
# delete(config.get_database_path())

print("--- %s seconds ---" % (time.time() - start_time))
