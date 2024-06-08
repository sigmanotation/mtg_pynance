from mtg_pynance.config import Config
from mtg_pynance.statistics import run_mtg_pynance
from pathlib import Path
import time

start_time = time.time()

workspace_path = Path("/Users/zachserikow/Desktop/pus")
collection_path = Path("/Users/zachserikow/Desktop/collection.csv")

config = Config(workspace_path, collection_path)

run_mtg_pynance(config)

print("--- %s seconds ---" % (time.time() - start_time))
