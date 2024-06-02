from datetime import datetime
from pathlib import Path
from tqdm import tqdm
import requests


def retrieve_bulk_data(bulk_info_file: Path, bulk_data_file: Path, timestamp):
    """
    Write Scryfall's bulk data default cards json file and its information json file
    at the target path. If these files already exist at the target path, they are
    overwritten if the current files hosted by Scryfall are newer.

    Note that Scryfall uses UTC timestamps.

    Parameters
    ----------
    config: mtg_pynance.config.Config
        Configuration defining run conditions.
    """
    # API call to Scryfall for its bulk data default cards information
    scryfall = "https://api.scryfall.com/bulk-data/default-cards"
    bulk_info_r = requests.get(scryfall, params={"format": "json"})
    bulk_info_j = bulk_info_r.json()

    # Check if local files exist and are older than Scryfall's
    if timestamp is not None:
        # Get Scryfall timestamp
        api_ts = bulk_info_j["updated_at"]
        api_dt = datetime.fromisoformat(api_ts)

        if timestamp >= api_dt:
            return

    # Write bulk info file
    with open(bulk_info_file, "wb") as f:
        f.write(bulk_info_r.content)

    # Write bulk data file
    print("Downloading Scryfall's bulk data default cards file...")
    url = bulk_info_j["download_uri"]
    bulk_data_r = requests.get(url, params={"format": "json"})
    with open(bulk_data_file, "wb") as f:
        f.write(bulk_data_r.content)

    # TODO the progress bar is nice, but slows it down a lot
    # url = bulk_info_j["download_uri"]
    # with requests.get(
    #     url, params={"format": "json"}, stream=True, headers={"Accept-Encoding": None}
    # ) as r:
    #     r.raise_for_status()
    #     with open(bulk_data_file, "wb") as f:
    #         pbar = tqdm(total=int(r.headers["Content-Length"]) / 1e6)
    #         for chunk in r.iter_content(chunk_size=8000):
    #             if chunk:  # filter out keep-alive new chunks
    #                 f.write(chunk)
    #                 pbar.update(len(chunk) / 1e6)
