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
Copy and paste this code into a new Python file and save it, naming the file whatever you wish. Next, activate the Python virtual environment you installed mtg_pynance to.