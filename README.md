# Overview

The `filebrowser-client` is an async client CLI and library for the [Filebrowser](https://github.com/filebrowser/filebrowser) API.

## Installation

The easiest way to install the `filebrowser-client` is to use `pip`:

```bash
    pip3 install filebrowser-client
```

## Features

-   [x] Download a remote file or a directory
-   [x] Upload a file or a directory to a remote location
-   [x] Delete a file or a directory from a remote location

## Usage

The `filebrowser-client` provides a cli client and a library to interact with the `Filebrowser` API.

### CLI

Run `filebrowser-client --help` to see the global options and the available commands.

```bash
    filebrowser-client --help
    Usage: filebrowser-client [OPTIONS] COMMAND [ARGS]...

    Options:
    --help  Show this message and exit.


    Commands:
    download  Download a file or a directory from a remote location
    upload    Upload a file or a directory to a remote location
    delete    Delete a file or a directory from a remote location
```

### Library

```python
    import asyncio
    from filebrowser_client import FilebrowserClient

    client = FilebrowserClient("http://localhost:8080", "admin", "admin")
    asyncio.run(client.connect())

    asyncio.run(client.download("/path/to/file", "/path/to/destination"))
```

## License

This project is licensed under the MIT License

## Development

The `filebrowser-client` is developed using `poetry` and `pre-commit`.
### Prerequisites

-   [Python 3.7+](https://www.python.org/downloads/)
-   [Poetry](https://python-poetry.org/docs/#installation)
-   [Pre-commit](https://pre-commit.com/#install)

### Setup

```bash
    poetry install
    pre-commit install
```
## Build

```bash
    poetry build
```
