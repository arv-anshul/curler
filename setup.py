import subprocess
from pathlib import Path

from setuptools import find_packages, setup

__project_name__ = "curler"
__license__ = "MIT"
__author__ = "arv-anshul"
__author_email__ = "arv.anshul.1864@gmail.com"
__author_github__ = "https://github.com/arv-anshul/"
__project_repo__ = "https://github.com/arv-anshul/curler/"

readme_path = Path("README.md")
requirements_path = Path("requirements.txt")

# --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- #
package_version = (
    subprocess.run(["git", "describe", "--tags"], stdout=subprocess.PIPE)
    .stdout.decode()
    .strip()
)

if "-" in package_version:
    v, i, s = package_version.split("-")
    package_version = v + "+" + i + ".git." + s

assert "-" not in package_version
assert "." in package_version
# --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- #

setup(
    name=__project_name__,
    version=package_version,
    description=(
        "Import curl command in python and use it with requests, httpx, etc. libraries."
    ),
    long_description=readme_path.read_text(),
    long_description_content_type="text/markdown",
    url=__project_repo__,
    license=__license__,
    author=__author__,
    author_email=__author_email__,
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    install_requires=[i.strip() for i in requirements_path.read_text().split("\n")],
    extras_require={
        "dev": ["twine>=4.0.2"],
    },
    python_requires=">=3.9",
)
