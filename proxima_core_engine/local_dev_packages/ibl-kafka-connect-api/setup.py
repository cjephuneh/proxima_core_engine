from glob import glob
from os.path import basename, splitext

from setuptools import find_packages, setup

setup(
    name="ibl-kafka-connect-api",
    version="1.0.1",
    description="CLI/API for interacting with the Kafka Connect REST API",
    packages=find_packages("src"),
    package_dir={"": "src"},
    include_package_data=True,
    py_modules=[splitext(basename(path))[0] for path in glob("src/*.py")],
    install_requires=[
        "factory-boy>=3.2.1",
        "requests>=2.28.1",
        "click>=8.1.3",
    ],
    entry_points={"console_scripts": ["konnect = kafka_connect.cli.cli:cli"]},
)
