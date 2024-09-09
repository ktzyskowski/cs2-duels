# src.processing.data

The main file in this package is `game.py`, which implements a wrapper object over the ESTA JSON data. I've chosen to
design wrapper classes rather than work directly with the JSON data because it allowed me to attach processing logic to
the pieces of data they were relevant to (such as the `Player.crosshair_placement_score` method). You can follow from
`game.py` to the remaining relevant files in the package.

`util.py` holds generic utility functions and classes which I didn't feel should live anywhere else.
