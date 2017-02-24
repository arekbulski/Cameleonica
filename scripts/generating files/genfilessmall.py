#!/usr/bin/python3
import sys, os, time, random

data = bytes(50*1024)
for i in range(10000):
    with open('files/%s' % i, 'wb') as f:
        f.write(data)

os.system('sync')
