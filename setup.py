from codecs import open
from os import path

from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))

with open(path.join(here, "README.rst"), "r") as f:
    long_description = f.read()

setup(
    name="gitea_client",
    version="1.0.9",
    description="A python library for interacting with a Gitea server",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/unfoldingWord-dev/python-gitea-client",
    author="unfoldingWord",
    author_email="dev@unfoldingword.org",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2.7",
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5'
    ],
    keywords=["gitea", "gogs", "http", "client"],
    packages=find_packages(),
    install_requires=["future", "requests", "attrs"],
    test_suite="tests"
)
