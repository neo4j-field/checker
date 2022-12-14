from setuptools import find_packages, setup

setup(
    name="checker",
    version="0.4.2",

    url="https://github.com/neo4j-field/checker",
    maintainer="Dave Voutila",
    maintainer_email="dave.voutila@neotechnology.com",
    license="Apache License 2.0",

    install_requires=[
        "pandas>=1.2.0",
	    "pyarrow>=7.0.0",
	    "graphdatascience>=1.3.0",
    ],
    packages=find_packages(),
)
