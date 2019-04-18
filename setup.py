from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="neopylib",  
    version="0.1.dev",
    author="Clément Trassoudaine",
    author_email="clement.trassoudaine@eurecom.fr",
    description="A pythonic Cypher queries generator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    keywords="neo4j cypher graph",
    url="https://github.com/intv0id/neopylib",
    packages=find_packages(),
    python_requires=">=3.6.6",
    install_requires=['dataclasses', 'itertools', 'string'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
 )