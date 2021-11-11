#!/bin/bash

CURDIR=$(cd `dirname $0` && pwd)

nohup /usr/bin/python $CURDIR/src/window.py > $CURDIR/data/log.txt &
