import argparse
import asyncio

from .client import FilebrowserClient
from .version import __version__

UPLOAD, DOWNLOAD, DELETE = "upload", "download", "delete"


def parse_args():
    parser = argparse.ArgumentParser(description="Filebrowser async client")
    parser.add_argument(
        "command", choices=(UPLOAD, DOWNLOAD, DELETE), help="Command to execute"
    )
    parser.add_argument("--version", action="version", version=__version__)
    parser.add_argument(
        "--host",
        default="http://localhost:8080",
        required=True,
        help="Filebrowser host",
    )
    parser.add_argument("--username", default="admin", help="Filebrowser username")
    parser.add_argument("--password", default="admin", help="Filebrowser password")
    parser.add_argument("--recaptcha", default="", help="Filebrowser recaptcha")
    parser.add_argument(
        "--insecure", action="store_true", help="Disable SSL verification"
    )
    parser.add_argument(
        "--concurrent", type=int, default=10, help="Number of concurrent requests"
    )
    parser.add_argument(
        "--override", action="store_true", help="Override existing files"
    )
    parser.add_argument("--source", help="Source file or directory")
    parser.add_argument("--destination", help="Destination file or directory")
    return parser.parse_args()


def main():
    args = parse_args()
    client = FilebrowserClient(
        host=args.host,
        username=args.username,
        password=args.password,
        recaptcha=args.recaptcha,
        insecure=args.insecure,
    )
    asyncio.run(client.connect())
    if args.command == UPLOAD:
        couroutine = client.upload(
            local_path=args.source,
            remote_path=args.destination,
            override=args.override,
            concurrent=args.concurrent,
        )
        for response in asyncio.run(couroutine):
            print(f"An upload to {response} is done successfully")
    elif args.command == DOWNLOAD:
        couroutine = client.download(
            local_path=args.destination, remote_path=args.source
        )
        for response in asyncio.run(couroutine):
            print(f"A download to {response} is done successfully")
    elif args.command == DELETE:
        couroutine = client.delete(remote_path=args.source)
        for response in asyncio.run(couroutine):
            print(f"The object {response} is removed successfully")
