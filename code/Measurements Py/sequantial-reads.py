#!/usr/bin/python
import sys, os, time, random

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
bufsize = BytesInt('64MB')
bufcount = 16
displaytimes = '-v' in sys.argv

print 'Buffer size: {0}  Buffer count: {1}  Total: {2}'.format(
    BytesString(bufsize), bufcount, BytesString(bufsize*bufcount))

os.system('echo noop | sudo tee /sys/block/sdb/queue/scheduler > /dev/null')
os.system('echo 3 | sudo tee /proc/sys/vm/drop_caches > /dev/null')

times = []
disk.seek(0)
disk.read(512)
for _ in range(bufcount):
    start = time.time()
    disk.read(bufsize)
    end = time.time()
    times.append(end-start)

avg = bufsize/(sum(times)/len(times))
print 'Average throughput: {0:0.0f} bytes/sec ({1:0.2f} megabytes/sec)'.format(avg, avg/1024/1024)
print 'Total time: {0:0.2f} sec'.format(sum(times))
if displaytimes:
    print 'Read times: {0} sec'.format(' '.join(['{0:0.4f}'.format(x) for x in times]))
