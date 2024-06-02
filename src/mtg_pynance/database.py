from datetime import datetime
from pathlib import Path
import requests
import json


def retrieve_database(target_path: Path):
    """
    Write Scryfall's bulk data default cards json file and its information json file
    at the target path. If these files already exist at the target path, they are
    overwritten if the current files hosted by Scryfall are newer.

    Note that Scryfall uses UTC timestamps.

    Parameters
    ----------
    target_path: Path
        Path to store Scryfall files at.
    """
    # Set up paths
    bulk_info_file = Path(target_path) / "bulk_default_info.json"
    bulk_data_file = Path(target_path) / "bulk_default_data.json"

    # API call to Scryfall for its bulk data default cards information
    scryfall = "https://api.scryfall.com/bulk-data/default-cards"
    bulk_info_r = requests.get(scryfall, params={"format": "json"})
    bulk_info_j = bulk_info_r.json()

    # Check if local files exist and are older than Scryfall's
    if bulk_info_file.exists():
        # Get timestamp of local file
        with open(bulk_info_file) as f:
            bulk_info_dict = json.load(f)
        local_ts = bulk_info_dict["updated_at"]
        local_dt = datetime.fromisoformat(local_ts)

        # Get Scryfall timestamp
        api_ts = bulk_info_j["updated_at"]
        api_dt = datetime.fromisoformat(api_ts)

        if local_dt >= api_dt:
            return

    # Write bulk info file
    with open(bulk_info_file, "wb") as f:
        f.write(bulk_info_r.content)

    # Write bulk data file
    url = bulk_info_j["download_uri"]
    bulk_data_r = requests.get(url, params={"format": "json"})
    with open(bulk_data_file, "wb") as file:
        file.write(bulk_data_r.content)
