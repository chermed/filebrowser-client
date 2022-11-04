# Overview

The `filebrowser-client` is an async client library for the [Filebrowser](https://github.com/filebrowser/filebrowser) API.
It provides a cli client and a library to interact with the API.

## Installation

The easiest way to install the `filebrowser-client` is to use `pip`:

```bash
    pip3 install filebrowser-client
```

## Features

-   [x] Download a file or a directory
-   [x] Upload a file or a directory
-   [x] Delete a file or a directory

## Usage

The `filebrowser-client` provides a cli client and a library to interact with the `Filebrowser` API.

### CLI

Run `filebrowser-client --help` to see the available commands.

```bash
    $ filebrowser-client --help
    usage: filebrowser-client [-h] [--version] --host HOST [--username USERNAME] [--password PASSWORD] [--recaptcha RECAPTCHA] [--insecure]
                            [--concurrent CONCURRENT] [--override] [--source SOURCE] [--destination DESTINATION]
                            {upload,download,delete}

    Filebrowser async client CLI

    positional arguments:
    {upload,download,delete}
                            Command to execute

    optional arguments:
    -h, --help            show this help message and exit
    --version             show program's version number and exit
    --host HOST           Filebrowser host
    --username USERNAME   Filebrowser username
    --password PASSWORD   Filebrowser password
    --recaptcha RECAPTCHA
                            Filebrowser recaptcha
    --insecure            Disable SSL verification
    --concurrent CONCURRENT
                            Number of concurrent requests
    --override            Override existing files
    --source SOURCE       Source file or directory
    --destination DESTINATION
                            Destination file or directory

```

### Library

```python
    import asyncio
    from filebrowser_client import FilebrowserClient

    client = FilebrowserClient("http://localhost:8080", "admin", "admin")
    asyncion.run(client.connect())

    asyncio.run(client.download("/path/to/file", "/path/to/destination"))
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## Development

The `filebrowser-client` is developed using `poetry`, `pre-commit` and `Pylint`.
### Prerequisites

-   [Python 3.8+](https://www.python.org/downloads/)
-   [Poetry](https://python-poetry.org/docs/#installation)
-   [Pre-commit](https://pre-commit.com/#install)
-   [Pylint](https://www.pylint.org/#install)

## Build

```bash
    poetry build
```
