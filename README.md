# Spigot

## Description
A trivial python async network client

## Usage
The package can be run directly from source as a module, e.g.
```
python -m spigot http://127.0.0.1:8080 --type=http --reqs 10 --msg "an http message"
```
And then run like so:
```
python -m spigot ...
```

Or built, and installed from source, e.g.
```
python3 -m build --wheel
...
pip install dist/spigot-0.1.0-py3-none-any.whl
```
And then run like so:
```
spigot ...
```

For more info on command line usage see `--help`.
```
spigot --help
```

## Development

### Automated Testing
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

### Manual Testing
There's also an echo server, located at `scripts/echo_server.py` for
manual testing.

The echo server can either be run as a standalone script
```
python scripts/echo-server.py ...
```

Or with the `echo-server` command, if installed via pip (see above)
```
echo-server ...
```

#### Examples:
First start the echo server
```
echo-server --type http --port 8080
```
Then in a separate terminal run the spigot client
```
spigot http://127.0.0.1:8080 --type=http --reqs 10 --msg "an http message"
```

