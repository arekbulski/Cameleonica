#!/usr/bin/python3
import sys, os, time, random

with open('file1', 'wb') as f:
    data = bytes(1024*1024)
    for i in range(0, int(2e9), len(data)):
        f.write(data)

os.system("sync")
