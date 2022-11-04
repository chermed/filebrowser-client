from setuptools import setup

from .filebrowser_client import __version__

with open("README.md", "r", encoding="utf-8").read() as readme_file:
    readme_content = readme_file.read()


packages = ["filebrowser_client"]

package_data = {"": ["*"]}

install_requires = ["aiohttp[speedups]>=3.8.3,<4.0.0"]

setup_kwargs = {
    "name": "filebrowser-client",
    "version": __version__,
    "description": "An async client for filebrowser",
    "long_description": readme_content,
    "author": "Mohamed Cherkaoui",
    "author_email": "chermed@gmail.com",
    "maintainer": "chermed@gmail.com",
    "maintainer_email": "chermed@gmail.com",
    "url": "https://github.com/chermed/filebrowser-client",
    "packages": packages,
    "package_data": package_data,
    "install_requires": install_requires,
    "python_requires": ">=3.8,<4.0",
}


setup(**setup_kwargs)
