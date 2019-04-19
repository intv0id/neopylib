from setuptools import setup, find_packages

VERSION="0.2.dev2"

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="neopylib",  
    version=VERSION,
    author="Clément Trassoudaine",
    author_email="clement.trassoudaine@eurecom.fr",
    description="A pythonic Cypher queries generator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    keywords="neo4j cypher graph",
    url="https://github.com/intv0id/neopylib",
    packages=find_packages(),
    include_package_data=True,
    python_requires=">=3.6.6",
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
 )