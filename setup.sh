#!/usr/bin/env bash
set -e
error() { 
    echo "Invoke this script with no arguments or '--no-venv' only."
    exit 1
}
if [ $# -gt 1 ]; then
    error
fi

if [[ $1 == "" ]]; then
    command -v virtualenv >/dev/null 2>&1 || { echo >&2 "virtualenv is required but it's not installed.  Aborting."; exit 1; }
    virtualenv venv
    source venv/bin/activate
elif [[ $1 != "--no-venv" ]]; then
    error
fi

pip3 install kivy Cython
garden install --app graph
garden install --app tickmarker
pushd libs/garden/garden.tickmarker
python setup.py build install
popd
echo -e "----------\nSUCCESS!\n"
