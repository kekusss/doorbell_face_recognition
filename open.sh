#!/bin/bash

if pidof -x "`basename $0`" -o $$ >/dev/null; then
    exit 0
fi

echo 'start'

sleep 10  # Waits 10 seconds.

echo 'stop'