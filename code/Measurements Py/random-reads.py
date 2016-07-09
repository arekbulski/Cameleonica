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

def BytesStringFloat(n):
    x = float(n)
    suffixes = ['B','KB','MB','GB','TB','PB','EB','ZB','YB']
    suffix = 0
    while x > 1024.0 and suffix+1 < len(suffixes):
        suffix += 1
        x /= 1024.0
    return '{0:0.2f}{1}'.format(x, suffixes[suffix])



disk = open('/dev/sdb', 'r')
disk.seek(0,2)
disksize = disk.tell()
os.system('echo noop | sudo tee /sys/block/sdb/queue/scheduler > /dev/null')

print 'Syntax: progam [-v]:  for verbose mode.'
print 'Disk name: {0}  Disk size: {1}  Scheduler disabled.'.format(
    disk.name, BytesStringFloat(disksize))



samplesize = 5
displaytimes = '-v' in sys.argv
displaysamplesize = 24

for randomareas in [False,True]:
    print
    print 'Measuring: Random seek time {0}'.format(
        'using random areas of disk.' if randomareas else 'using beginning of disk.')
    print 'Sample size: {0} {1}'.format(
        samplesize, '(displayed {0})'.format(displaysamplesize) if randomareas else '')

    for area in [BytesInt('1MB')*2**i for i in range(0,64)]+[disksize]:
        if disksize < area:
            break

        os.system('echo 3 | sudo tee /proc/sys/vm/drop_caches > /dev/null')

        times = []
        disk.seek(0)
        disk.read(512)
        for _ in range(samplesize):
            left = random.randint(0, disksize-area) if randomareas else 0
            right = left + random.randint(0, area)
            disk.seek(left)
            disk.read(512)
            start = time.time()
            disk.seek(right)
            disk.read(512)
            finish = time.time()
            times.append(finish-start)

        times = sorted(times)[:samplesize*95/100]
        print 'Area tested: {0:5}   Average: {1:3.2f} ms   Max: {2:3.2f} ms   Sum: {3:0.2f} sec'.format(
            BytesString(area), sum(times)/len(times)*1000, max(times)*1000, sum(times))
        if displaytimes:
            print 'Read times: {0} ... {1} ms'.format(
                ' '.join(['{0:0.2f}'.format(x*1000) for x in times[:displaysamplesize/2]]), 
                ' '.join(['{0:0.2f}'.format(x*1000) for x in times[-displaysamplesize/2:]]))



bufsize = BytesInt('64MB')
bufcount = 16

print
print 'Measuring: Sequential read throughput {0}'.format(
    'using random areas of disk.' if randomareas else 'using beginning of disk.')
print 'Buffer size: {0}  Buffer count: {1}  Total: {2}'.format(
    BytesString(bufsize), bufcount, BytesString(bufsize*bufcount))

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
print 'Average throughput: {0}/sec'.format(
    BytesStringFloat(avg))
print 'Total time: {0:0.2f} sec'.format(sum(times))
if displaytimes:
    print 'Read times: {0} sec'.format(' '.join(['{0:0.4f}'.format(x) for x in times]))
