#!/bin/bash -ex

if [ ! -z $(which flake8) ]; then
    flake8
fi

nosetests
