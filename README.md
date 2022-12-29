# Spigot

## Description
A trivial python async network client

## Usage
The package can be run directly from source as a module, e.g.
```
python -m spigot http://127.0.0.1:8080 --type=http --reqs 10 --msg "an http message"
```

Or built, and installed from source, e.g.
```
python3 -m build --wheel
...
pip install dist/spigot-0.1.0-py3-none-any.whl
```

For more info on command line usage see `--help`.
```
python -m spigot --help
```

## Development
To run tests...

First, install dev dependencies:
```
pip install -r requirements-dev.txt
...
```
Then, run tests using pytest:
```
pytest
...
```
