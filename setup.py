from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))


with open(path.join(here, "README.rst"), "r") as f:
    long_description = f.read()

setup(
    name="gogs_client",
    version="1.0.3",
    description="A python library for interacting with a gogs server",
    long_description=long_description,
    url="https://github.com/unfoldingWord-dev/python-gogs-client",
    author="unfoldingWord",
    author_email="ethantkoenig@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2.7",
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5'
    ],
    keywords=["gogs", "http", "client"],
    packages=find_packages(),
    install_requires=["future", "requests"],
    test_suite="tests"
)
