#!/bin/bash -ex

if [ $(python -c 'import sys; print(sys.version[:3])') == '3.6' ]; then
   pip install flake8
fi

pip install -r requirements.txt

pip install .
