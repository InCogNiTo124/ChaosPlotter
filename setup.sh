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

pip3 install pyqt5 matplotlib
echo -e "----------\nSUCCESS!\n"
