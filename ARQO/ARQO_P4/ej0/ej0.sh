#!/bin/bash

cat /proc/cpuinfo | grep 'cpu cores\|siblings\|model name\|cpu MHz' | sort | uniq -c

lstopo