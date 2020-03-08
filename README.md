# Game of Life

A Python implementation of Conway's Game of Life using a toroidal array to
represent 2-D space.

## Development

```console
# Create a virtual environment (optional):
$ mkdir -p "$HOME/.venvs"
$ python -m venv "$HOME/.venvs/python-conway"

# Install dependencies:
$ make deps

# Run tests:
$ make test

# Format code before you commit:
$ make fmt

# Format code + run all checks (recommended):
$ make check

# Run the app:
$ make run
```

See the [Makefile](./Makefile) for details.
