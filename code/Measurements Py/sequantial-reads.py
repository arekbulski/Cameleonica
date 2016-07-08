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
    if all(c in '0123456789' for c in s):
        return int(s)
    suffixes = ['B','KB','MB','GB','TB','PB','EB','ZB','YB']
    for power,suffix in reversed(list(enumerate(suffixes))):
        if s.endswith(suffix):
            return int(s.rstrip(suffix))*1024**power
    raise ValueError('BytesInt requires proper suffix ('+' '.join(suffixes)+').')

disk = open('/dev/sdb', 'r')
disksize = BytesInt('1TB')
bufsize = BytesInt('16MB')
print 'Entire disk size: ', BytesString(disksize), ' Buffer size: ', BytesString(bufsize)

os.system('echo noop | sudo tee /sys/block/sdb/queue/scheduler > /dev/null')
os.system('echo 3 | sudo tee /proc/sys/vm/drop_caches > /dev/null')

times = []
disk.seek(0)
for _ in range(20):
    start = time.time()
    disk.read(bufsize)
    end = time.time()
    times.append(end-start)

print 'Read times: ', ', '.join(['{0:0.4f}'.format(x) for x in times]), ' in seconds'
print 'Average throughput: {0:0.0f} bytes/sec'.format(bufsize/(sum(times)/len(times)))
