#!/bin/bash

export PATH="$HOME/miniconda/bin:$PATH"
source activate test

pytest -x -vv --cov=qtawesome --cov-report=term-missing qtawesome

if [ $? -ne 0 ]; then
    exit 1
fi

codecov
