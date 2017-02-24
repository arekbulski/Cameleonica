#!/usr/bin/python3
import sys, os, time, random

data = bytes(10)
for i in range(200*1000):
    with open('files/%s' % i, 'wb') as f:
        f.write(data)

os.system('sync')
