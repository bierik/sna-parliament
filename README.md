# sna-parliament

Analysis of the swiss parliament using graph metrics. Datasource is lobbywatch.ch.

## Installation

Install pipenv -> https://pypi.org/project/pipenv/

Install project dependencies

```bash
pipenv install
```

## Usage

### Seeding

Fetch lobbywatch to local sqlite database:

```python
from seed import seed

seed()
```

This command will fetch all parliamentarians, organisations, lobby groups and connections between the parliamentarians the organisations and lobby groups.
The graphql endpoint of lobbywatch is not capable of resolving those connections in one query.
So the script scrapes the data bit and bit and makes the connection in an sqlite database.
This database also provides a cache for further data cleanup steps.

The default database is `data.db`. The database can be changed using the `SNA_DATABASE` environment variable.

To update the data, run the seeding process again. Existing data will not be lost but added.

### Normalization

Some organisations need to be normalized. For example, `Schweizerische Volkspartei` is mapped to `Schweizerische Volkapartei Kanton Bern`.
We want this, so organisations can be grouped together.

```python
from normalize import normalize

normalize()
```

The normalization step is done in place. Meaning that the currently connected database is normalized and the doubled entries are lost. To prevent this behaviour, copy the initially seeded database and do the normalization step on the copy.

### Generating network

We use [gephi](https://gephi.org/) to properly visualize the graph.

```python
from network import generate_networks

generate_networks()
```

The `generate_networks` function will generate two `.gexf` files. The `lobby_group.gexf`-file contains a weighted bipartite graph with all parliamentarians connected to the lobby groups.
The `organisations.gexf`-file contains a weighted bipartite graph with all parliamentarians connected to the organisations.

### Network Analysis

To generate all analyzes as a `.csv` file.

```python
from analyse import generate_analysis

generate_analysis()
```

### Main Script

To run all steps at once, run the `main.py` file with python.

```bash
pipenv run python main.py
```
