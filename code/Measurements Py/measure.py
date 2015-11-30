#!/usr/bin/python
import os, time, random

def BytesString(n):
    suffixes = ['B','KB','MB','GB','TB','PB','EB','ZB','YB']
    suffix = 0
    while n % 1024 == 0 and suffix+1 < len(suffixes):
        suffix += 1
        n /= 1024
    return '{0}{1}'.format(n, suffixes[suffix])

def BytesInt(s):
    suffixes = ['B','KB','MB','GB','TB','PB','EB','ZB','YB']
    for power,suffix in reversed(list(enumerate(suffixes))):
        if s.endswith(suffix):
            return int(s.rstrip(suffix))*1024**power
    raise ValueError('BytesInt requires proper suffix ('+' '.join(suffixes)+').')

disk = open('/dev/sdb', 'r')
disksize = BytesInt('1TB')
print 'Entire disk has size: ', BytesString(disksize)

for area in map(BytesInt, '1MB 4MB 16MB 128MB 1GB 4GB 16GB 128GB 1TB'.split()):
    os.system('echo noop | sudo tee /sys/block/sdb/queue/scheduler > /dev/null')
    os.system('echo 3 | sudo tee /proc/sys/vm/drop_caches > /dev/null')

    times = []
    for _ in range(5000):
        left = random.randint(0, disksize-area)
        right = left + random.randint(0, area)
        disk.seek(left)
        disk.read(512)
        start = time.time()
        disk.seek(right)
        disk.read(512)
        end = time.time()
        point = (end-start)
        times.append(point)

    times = sorted(times)[:4750]
    print 'Area tested: {0:5}  Average: {1:6f}sec  Max: {2:6f}sec  Sum: {3:2f}sec'.format(
        BytesString(area), sum(times)/len(times), max(times), sum(times))
