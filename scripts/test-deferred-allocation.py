#!/usr/bin/python3
import sys, os, time, random

os.system('trash file1')
os.system('sync')

with open('file1','wb') as f:
    print('Recreated test tile.')
    print('Written and synced piece: ', end='')

    data = bytes(256*1024)
    for i in range(30):
        f.write(data)
        f.flush()
        os.system('sync')
        #os.system('echo 3 | sudo tee /proc/sys/vm/drop_caches > /dev/null')
        time.sleep(10)
        print('.', end=' ', flush=1)
    print()

os.system('filefrag file1')
