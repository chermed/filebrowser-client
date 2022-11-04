import asyncio
import os
import shutil
import tempfile
import zipfile
from typing import Dict, List, Optional, Union

import aiohttp


def get_api_url(url: str) -> str:
    url = url.rstrip("/")
    if not url.endswith("/api"):
        url = url + "/api"
    return url


def require_string(value: str, name: str) -> str:
    if value is None:
        raise ValueError(f"the {name} is required")
    return value.strip()


class FilebrowserClient:
    def __init__(
        self,
        host: str,
        username: str = "",
        password: str = "",
        recaptcha: str = "",
        insecure: bool = False,
    ) -> None:
        self.api_url = get_api_url(host)
        self.login_api_url = self.api_url + "/login"
        self.resources_api_url = self.api_url + "/resources"
        self.raw_api_url = self.api_url + "/raw"
        self.username = username
        self.password = password
        self.recaptcha = recaptcha
        self.insecure = insecure
        self.token: Union[str, None] = None

    def get_headers(self, extras: Optional[Dict] = {}) -> dict:
        headers = {
            "X-Auth": self.token,
            "Authorization": f"Bearer {self.token}",
        }
        if extras:
            headers.update(extras)
        return headers

    async def connect(self) -> str:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                self.login_api_url,
                json={
                    "username": self.username,
                    "password": self.password,
                    "recaptcha": self.recaptcha,
                },
                verify_ssl=not self.insecure,
            ) as response:
                response.raise_for_status()
                self.token = await response.text()
                return self.token

    # Uploading the files

    async def _upload_file(
        self, local_path: str, remote_path: str, override: bool = False
    ) -> str:
        async with aiohttp.ClientSession() as session:
            resource_api = self.resources_api_url + "/" + remote_path
            extra_headers = {"Content-Type": "application/octet-stream"}
            headers = self.get_headers(extra_headers)
            params = {"override": "true" if override else "false"}
            data = open(local_path, "rb")
            async with session.post(
                resource_api,
                headers=headers,
                data=data,
                params=params,
                verify_ssl=not self.insecure,
            ) as response:
                response.raise_for_status()
                return resource_api

    async def _upload_dir(
        self,
        local_path: str,
        remote_path: str,
        override: bool = False,
        concurrent: int = 100,
    ) -> List[str]:
        requests = []
        local_path = local_path.rstrip("/")
        response: List[str] = []
        if not concurrent:
            concurrent = 100
        for root, _, files in os.walk(local_path):
            for file in files:
                local_file_path = os.path.join(root, file)
                remote_file_path = os.path.join(
                    remote_path, os.path.relpath(local_file_path, local_path)
                )
                requests.append(
                    self._upload_file(
                        local_file_path, remote_file_path, override=override
                    )
                )
                if len(requests) == concurrent:
                    response.extend(await asyncio.gather(*requests))
                    requests = []
        response.extend(await asyncio.gather(*requests))
        return response

    async def upload(
        self,
        local_path: str,
        remote_path: str,
        override: bool = False,
        concurrent: int = 10,
    ) -> str:
        local_path = require_string(local_path, "source")
        remote_path = require_string(remote_path, "destination")
        if not os.path.exists(local_path):
            raise FileNotFoundError("Local path does not exist")
        remote_path = remote_path.lstrip("/")
        if os.path.isdir(local_path):
            remote_path = remote_path.rstrip("/")
            return await self._upload_dir(
                local_path=local_path,
                remote_path=remote_path,
                override=override,
                concurrent=concurrent,
            )
        if os.path.isfile(local_path):
            if remote_path.endswith("/"):
                remote_path = remote_path + os.path.basename(local_path)
            return [
                await self._upload_file(
                    local_path=local_path, remote_path=remote_path, override=override
                )
            ]
        raise FileNotFoundError("Local path is not a file or directory")

    # Downloading the files

    async def _download_zip(self, local_path: str, remote_path: str) -> List[str]:
        with tempfile.NamedTemporaryFile() as temp_zip_file:
            async with aiohttp.ClientSession() as session:
                remote_path = remote_path.lstrip("/")
                raw_api = self.raw_api_url + "/" + remote_path
                extra_headers = {"Content-Type": "application/octet-stream"}
                headers = self.get_headers(extra_headers)
                params = {"algo": "zip"}
                async with session.get(
                    raw_api,
                    headers=headers,
                    params=params,
                    verify_ssl=not self.insecure,
                ) as response:
                    response.raise_for_status()
                    content_type = response.headers["Content-Type"]
                    with open(temp_zip_file.name, "wb+") as tmp_file:
                        while True:
                            chunk = await response.content.read(1024)
                            if not chunk:
                                break
                            tmp_file.write(chunk)
                    with tempfile.TemporaryDirectory() as temp_dir:
                        if content_type.strip().lower().startswith("application/zip"):
                            with zipfile.ZipFile(temp_zip_file.name, "r") as zip_ref:
                                zip_ref.extractall(temp_dir)
                        else:
                            filename = os.path.basename(remote_path)
                            shutil.copy(
                                temp_zip_file.name, os.path.join(temp_dir, filename)
                            )
                        return [
                            shutil.copytree(temp_dir, local_path, dirs_exist_ok=True)
                        ]

    async def download(self, local_path: str, remote_path: str) -> List[str]:
        local_path = require_string(local_path, "destination")
        remote_path = require_string(remote_path, "source")
        if os.path.exists(local_path) and not os.path.isdir(local_path):
            raise FileExistsError("Local path is not a directory")
        if not os.path.exists(local_path):
            os.makedirs(local_path, exist_ok=True)
        remote_path = remote_path.strip("/")
        return await self._download_zip(local_path=local_path, remote_path=remote_path)

    ## Deleting the files

    async def delete(self, remote_path: str) -> List[str]:
        remote_path = require_string(remote_path, "path")
        async with aiohttp.ClientSession() as session:
            remote_path = remote_path.lstrip("/")
            resource_api = self.resources_api_url + "/" + remote_path
            headers = self.get_headers()
            async with session.delete(resource_api, headers=headers) as response:
                response.raise_for_status()
                return [resource_api]
