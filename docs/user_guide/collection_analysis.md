After executing the run file, the only thing that remains is to analyze your collection's price data! The price data is stored in the local SQL database made by mtg_pynance. With this data, a multitude of possible analyses can be performed on your collection. Check out the [analysis functions](../api/analysis.md) that come with mtg_pynance for an idea. Here we illustrate one possible way to evaluate your collection's gain/loss using the builtin `#!python collection_stats` function, but we also discuss more advanced possible analyses.

## Example
### Calculating your collection's gain/loss

For this example, we use a Jupyter notebook and the Plotly library. To install Jupyter, see [here](https://jupyter.org/). For Plotly, check [this](https://plotly.com/python/) out. Note that you will also have to install

mtg_pynance comes with the built-in analysis function `#!python collection_stats` to compute your collection's total value and gain/loss as a function of time. Make a Jupyter file and paste each block of the below code into its own cell in the file.

```python
from mtg_pynance.config import Config
from mtg_pynance.analysis import collection_stats
from pathlib import Path
from plotly.subplots import make_subplots
import plotly.graph_objects as go
```
```python
workspace_path = Path("/to/your/workspace/directory")
collection_path = Path("/to/your/collection/csv/file")

config = Config(workspace_path, collection_path)

df = collection_stats(config.get_database_path())
```
Run the notebook, noting that we have stored the results of `#!python collection_stats` in the variable `#!python df`. `#!python collection_stats` returns a [Polars](https://pola.rs/) dataframe that contains three columns: timestamp, market_value, and gain/loss. You could print `#!python df` to view your collection's statistics, but we can do better. Let's plot it using Plotly.

In a subsequent cell, paste the code below.

```python
dfd = df.to_dict(as_series=False)

fig = make_subplots()
fig.add_trace(
    go.Scatter(
        x=dfd['timestamp'],
        y=dfd['gain/loss'], 
        mode='lines+markers',
    )
)
fig.update_layout(
    xaxis_title="Time (UTC)",
    yaxis_title="Gain/loss (USD)",
)
```

Running this cell produces a graph of your collection's gain/loss as a function of time! Some easy modifications to this plotting code allow you to plot your collection's value versus time as well.

## Advanced example
### Calculating the gain/loss of artifacts in your collection

WIP: will update in due time!