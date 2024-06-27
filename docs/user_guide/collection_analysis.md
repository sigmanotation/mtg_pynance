After executing the run file, the only thing that remains is to analyze your collection's price data! The price data is stored in the local SQL database made by mtg_pynance. With this data, a multitude of possible analyses can be performed on your collection. Here we illustrate one possible way to evaluate your collection's value, but we also discuss more advanced analysis that can be added in by the user. 

## Example: calculating your collection's value

For this example, we use a Jupyter notebook. To install Jupyter, see [here](https://jupyter.org/).

mtg_pynance comes with the built-in analysis function collection_stats to compute your collection's total value and gain/loss as a function of time. Make a Jupyter file and paste the below code to the file.

```python
from mtg_pynance.config import Config
from mtg_pynance.analysis import collection_stats
from pathlib import Path


workspace_path = Path("/to/your/workspace/directory")
collection_path = Path("/to/your/collection/csv/file")

config = Config(workspace_path, collection_path)

df = collection_stats(config.get_database_path())
```


Disclaimer on other uses collection_stats(config.get_database_path())