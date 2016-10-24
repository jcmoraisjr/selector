#!/bin/sh
# Process doesn't stop on sigterm if running as PID 1
python -u selector.py "$@" &
trap "kill -term $!" TERM
wait
