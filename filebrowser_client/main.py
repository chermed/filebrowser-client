import asyncio

import fire
from colorama import Fore, Style

from .client import FilebrowserClient
from .version import __version__


class FilebrowserCli:
    """A CLI for Filebrowser"""

    def __init__(
        self,
        host,
        username: str = "",
        password: str = "",
        recaptcha: str = "",
        insecure: bool = False,
    ):
        self.client = FilebrowserClient(
            host=host,
            username=username,
            password=password,
            recaptcha=recaptcha,
            insecure=insecure,
        )

    def download(self, remote_path: str, local_path: str):
        """download a remote file or directory to local."""
        asyncio.run(self.client.connect())
        couroutine = self.client.download(
            local_path=local_path, remote_path=remote_path
        )
        asyncio.run(couroutine)
        print(
            Fore.GREEN
            + f"the download of {remote_path} to {local_path} is done successfully"
            + Style.RESET_ALL
        )

    def upload(
        self,
        local_path: str,
        remote_path: str,
        override: bool = False,
        concurrent: int = 10,
    ):
        """upload a local file or directory to filebrowser."""
        asyncio.run(self.client.connect())
        couroutine = self.client.upload(
            local_path=local_path,
            remote_path=remote_path,
            override=override,
            concurrent=concurrent,
        )
        asyncio.run(couroutine)
        print(
            Fore.GREEN
            + f"the upload of {local_path} to {remote_path} is done successfully"
            + Style.RESET_ALL
        )

    def delete(self, path: str):
        """delete a remote file or directory."""
        asyncio.run(self.client.connect())
        couroutine = self.client.delete(remote_path=path)
        for response in asyncio.run(couroutine):
            print(
                Fore.GREEN
                + f"The object {response} is removed successfully"
                + Style.RESET_ALL
            )


def main():
    """The main function."""
    fire.Fire(FilebrowserCli)


if __name__ == "__main__":
    main()
