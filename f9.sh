#!/usr/bin/env bash

# Automatically run project when vim saves with f9

## Kill existing tool
kill -9 `cat f9.pid`
## Slap the thing away from my main monitor
## Run anew, save pid for later
app &
echo $! > f9.pid
