## Instructions

After you have made your collection's CSV file, it is time to run mtg_pynance! To do this, we create a simple Python script that imports the needed objects from the mtg_pynance library as shown below.

```python
from mtg_pynance.config import Config
from mtg_pynance.database import run_mtg_pynance
from pathlib import Path


workspace_path = Path("/to/your/workspace/directory")
collection_path = Path("/to/your/collection/csv/file")

config = Config(workspace_path, collection_path)

if __name__ == "__main__":
    run_mtg_pynance(config)
```
Copy and paste this code into a new Python file and save it, naming the file whatever you wish. Make sure to change the workspace_path and collection_path! The workspace_path is the path to the directory that stores your local SQL database along with the downloaded Scryfall files. The collection_path is the path to your Magic the Gathering card collection CSV file.

Next, activate the Python virtual environment you installed mtg_pynance to. Inside that environment, simply command Python to run your script.