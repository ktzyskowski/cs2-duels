# src.processing.data

The main file in this package is `game.py` which holds the wrapper classes over the ESTA data. These wrapper
classes help serve to query relevant information for feature extraction.

- `game.Game` wraps over an individual game/map played, and holds a list of rounds as well as various metadata.
- `game.Round` wraps over an individual round played during a game, and holds frame information for each player as well
  as parsed kill events.
- `game.Kill` wraps over the kill events in the ESTA data.

`frame.py` holds wrapper classes over individual frame data for teams and their players, as well as additional
querying logic.

`util.py` holds utility functions and classes that could be abstracted away from the ESTA data pipeline.
