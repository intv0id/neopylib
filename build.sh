#! /bin/bash

# Build
pipenv lock -r > requirements.txt
python setup.py sdist

# Clean
rm requirements.txt
