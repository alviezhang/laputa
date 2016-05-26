#!/bin/sh

PWD=`pwd`

source env/bin/activate
python -m laputa -c laputa.toml
