#!/usr/bin/env bash

if [ -z ${1+x} ]; then
    echo "No file argument supplied. Exiting..."
    exit 1
fi

FILE=$1
realpath $FILE
echo "binary"
base64 $FILE
