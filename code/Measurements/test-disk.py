#!/usr/bin/python3
import sys, os, time, timeit, random, ctypes


#--------------------------------------------------------------------------------------------------

def BytesString(n):
    suffixes = ['B','KB','MB','GB','TB','PB','EB','ZB','YB']
    suffix = 0
    while n % 1024 == 0 and suffix+1 < len(suffixes):
        suffix += 1
        n //= 1024
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


#--------------------------------------------------------------------------------------------------

if len(sys.argv) < 2:
    print('Syntax: program /dev/sda > log')
    print('Path can also use /dev/disk/by-id/  by-label/  by-path/  by-uuid/')
    print('Redirect to a log file is optional.')
    sys.exit()

dev = os.path.realpath(sys.argv[1]).split('/')[-1]
disk = open('/dev/%s' % dev, 'rb')
disksize = disk.seek(0, 2)
os.system('echo noop | sudo tee /sys/block/%s/queue/scheduler > /dev/null' % dev)

print('Disk name: {0}  Disk size: {1}  Scheduler disabled.'.format(
    disk.name, BytesStringFloat(disksize)))


#--------------------------------------------------------------------------------------------------

libc = ctypes.CDLL(None, use_errno=True)

def readahead(fileno, offset, count):
    libc.readahead(ctypes.c_int(fileno), ctypes.c_longlong(offset), ctypes.c_size_t(count))

bufsize = 512
bufcount = 100

print()
print('Measuring: Concurrent random seek time using readahead.')
print('Samples: {0}   Sample size: {1}'.format(
    bufcount, bufsize))

for area in [BytesInt('1MB')*2**i for i in range(0,64)]+[disksize]:
    if area > disksize:
        continue

    os.system('echo 3 | sudo tee /proc/sys/vm/drop_caches > /dev/null')

    offsets = [random.randint(0, area-bufsize) for i in range(bufcount)]

    for i in offsets:
        readahead(disk.fileno(), i, bufsize)

    times = [timeit.timeit(lambda: os.pread(disk.fileno(), bufsize, i), number=1) for i in offsets]

    print('Area tested: {0:6}   Average: {1:5.2f} ms   Max: {2:5.2f} ms   Total: {3:0.2f} sec'.format(
        BytesString(area) if area < disksize else BytesStringFloat(area), 
        sum(times)/len(times)*1000, max(times)*1000, sum(times)))


#--------------------------------------------------------------------------------------------------

bufsize = 512
bufcount = 100

print()
print('Measuring: Random seek time using beginning of disk.')
print('Samples: {0}   Sample size: {1}'.format(
    bufcount, bufsize))

for area in [BytesInt('1MB')*2**i for i in range(0,64)]+[disksize]:
    if area > disksize:
        continue

    os.system('echo 3 | sudo tee /proc/sys/vm/drop_caches > /dev/null')

    offsets = [random.randint(0, area-bufsize) for i in range(bufcount)]

    os.pread(disk.fileno(), bufsize, 0)
    times = [timeit.timeit(lambda: os.pread(disk.fileno(), bufsize, i), number=1) for i in offsets]

    print('Area tested: {0:6}   Average: {1:5.2f} ms   Max: {2:5.2f} ms   Total: {3:0.2f} sec'.format(
        BytesString(area) if area < disksize else BytesStringFloat(area), 
        sum(times)/len(times)*1000, max(times)*1000, sum(times)))


#--------------------------------------------------------------------------------------------------

print()
print('Measuring: Random read throughput with various sizes.')

for i in range(8):
    bufsize = BytesInt('1MB')*2**i
    bufcount = int(128/((4/3)**i))

    os.system('echo 3 | sudo tee /proc/sys/vm/drop_caches > /dev/null')

    offsets = [random.randint(0, disksize-bufsize) for i in range(bufcount)]

    times = [timeit.timeit(lambda: os.pread(disk.fileno(), bufsize, i), number=1) for i in offsets]

    avg = bufsize/(sum(times)/len(times))
    print('Buffer: {0:4}   Average: {1:8}/sec   Samples: {2:3}   Total: {3:0.2f} sec'.format(
        BytesString(bufsize), BytesStringFloat(avg), bufcount, sum(times)))


#--------------------------------------------------------------------------------------------------

print()
print('Measuring: Sequential read throughput using beginning of disk.')

bufsize = BytesInt('10MB')
bufcount = 100

os.system('echo 3 | sudo tee /proc/sys/vm/drop_caches > /dev/null')

disk.seek(0)
times = [timeit.timeit(lambda: disk.read(bufsize), number=1) for i in offsets]

avg = bufsize/(sum(times)/len(times))
print('Buffer: {0:4}   Average: {1:8}/sec   Samples: {2:3}   Total: {3:0.2f} sec'.format(
    BytesString(bufsize), BytesStringFloat(avg), bufcount, sum(times)))


#--------------------------------------------------------------------------------------------------

os.system('echo cfq | sudo tee /sys/block/%s/queue/scheduler > /dev/null' % dev)

print()
print('Returned disk scheduler to CFQ.')

