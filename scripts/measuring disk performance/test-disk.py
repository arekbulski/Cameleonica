#!/usr/bin/python3
import sys, os, time, random, ctypes


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

libc = ctypes.CDLL(None, use_errno=True)

def readahead(fileno, offset, count):
    libc.readahead(ctypes.c_int(fileno), ctypes.c_longlong(offset), ctypes.c_size_t(count))


#--------------------------------------------------------------------------------------------------

def timeit2(resetfunc, func, mintotal=5.0):
    total = 0
    times = []
    while True:
        t1 = time.perf_counter()
        x = resetfunc()
        t2 = time.perf_counter()
        func(x)
        t3 = time.perf_counter()
        times.append(t3-t2)
        total += t3-t1
        if total >= mintotal:
            return times

def timeit3(resetfunc, func, arguments):
    times = []
    for arg in arguments:
        resetfunc(arg)
    for arg in arguments:
        t1 = time.perf_counter()
        func(arg)
        t2 = time.perf_counter()
        times.append(t2-t1)
    return times


#--------------------------------------------------------------------------------------------------

import functools
print = functools.partial(print, flush=True)


#--------------------------------------------------------------------------------------------------

if len(sys.argv) < 2:
    print('Syntax: sudo ./test-disk.py /dev/sda | tee log')
    print('Path can also use /dev/disk/by-id/  by-label/  by-path/  by-uuid/')
    print('Redirect to a log file is optional.')
    sys.exit()

dev = os.path.realpath(sys.argv[1]).split('/')[-1]
disk = open('/dev/%s' % dev, 'rb')
disksize = disk.seek(0, 2)
os.system('echo none | sudo tee /sys/block/%s/queue/scheduler > /dev/null' % dev)
print('Disk name: {0}  Disk size: {1}  Scheduler disabled.'.format(disk.name, BytesStringFloat(disksize)))


#--------------------------------------------------------------------------------------------------

bufsize = 512

print()
print('Measuring: Seek times when track buffer is working forwards.')
print('Buffer size: 512 bytes')

for areasize in [BytesInt('1MB')*(2**i) for i in range(0,64)] + [disksize]:
    if areasize > disksize:
        continue

    os.system('echo 3 | sudo tee /proc/sys/vm/drop_caches > /dev/null')

    def resetfunc():
        offset = random.randrange(0, areasize-2*bufsize)
        os.pread(disk.fileno(), bufsize, offset)
        return offset
    def func(offset):
        os.pread(disk.fileno(), bufsize, offset+bufsize)
    times = timeit2(resetfunc, func)

    print('Area size: {:6}   Average: {:6.2f} ms   Max: {:6.2f} ms'.format(
        BytesString(areasize) if areasize < disksize else BytesStringFloat(areasize),
        sum(times)/len(times)*1000, max(times)*1000 ))


#--------------------------------------------------------------------------------------------------

bufsize = 512

print()
print('Measuring: Seek times when track buffer is working backwards.')
print('Buffer size: 512 bytes')

for areasize in [BytesInt('1MB')*(2**i) for i in range(0,64)] + [disksize]:
    if areasize > disksize:
        continue

    os.system('echo 3 | sudo tee /proc/sys/vm/drop_caches > /dev/null')

    def resetfunc():
        offset = random.randrange(bufsize, areasize-bufsize)
        os.pread(disk.fileno(), bufsize, offset)
        return offset
    def func(offset):
        os.pread(disk.fileno(), bufsize, offset-bufsize)
    times = timeit2(resetfunc, func)

    print('Area size: {:6}   Average: {:6.2f} ms   Max: {:6.2f} ms'.format(
        BytesString(areasize) if areasize < disksize else BytesStringFloat(areasize),
        sum(times)/len(times)*1000, max(times)*1000 ))


#--------------------------------------------------------------------------------------------------

bufsize = 512

print()
print('Measuring: Seek times of random reads made in sequence (no readahead) over some area.')
print('Buffer size: 512 bytes')

for areasize in [BytesInt('1MB')*(2**i) for i in range(0,64)] + [disksize]:
    if areasize > disksize:
        continue

    os.system('echo 3 | sudo tee /proc/sys/vm/drop_caches > /dev/null')
    
    def resetfunc():
        return random.randrange(0, areasize-bufsize)
    def func(offset):
        os.pread(disk.fileno(), bufsize, offset)
    times = timeit2(resetfunc, func)

    print('Area size: {:6}   Average: {:5.2f} ms   Min: {:5.2f} ms   Max: {:5.2f} ms'.format(
        BytesString(areasize) if areasize < disksize else BytesStringFloat(areasize),
        sum(times)/len(times)*1000, min(times)*1000, max(times)*1000))


#--------------------------------------------------------------------------------------------------

bufsize = 512
bufcount = 100

print()
print('Measuring: Seek times of random reads made concurrently (using readahead) over some area.')
print('Buffer count: {0}   Buffer size: {1}'.format(bufcount, bufsize))

for area in [BytesInt('1MB')*(2**i) for i in range(0,64)] + [disksize]:
    if area > disksize:
        continue

    os.system('echo 3 | sudo tee /proc/sys/vm/drop_caches > /dev/null')

    offsets = [random.randrange(0, area-bufsize) for i in range(bufcount)]
    def resetfunc(offset):
        readahead(disk.fileno(), offset, bufsize)
    def func(offset):
        os.pread(disk.fileno(), bufsize, offset)
    times = timeit3(resetfunc, func, offsets)

    print('Area size: {:6}   Average: {:5.2f} ms   Min: {:5.2f} ms   Max: {:5.2f} ms'.format(
        BytesString(area) if area < disksize else BytesStringFloat(area),
        sum(times)/len(times)*1000, min(times)*1000, max(times)*1000))


#--------------------------------------------------------------------------------------------------

print()
print('Measuring: Random read throughput with various buffer sizes.')

for bs in ['1MB','2MB','4MB','8MB','16MB','32MB','64MB','128MB','256MB']:
    os.system('echo 3 | sudo tee /proc/sys/vm/drop_caches > /dev/null')

    bufsize = BytesInt(bs)
    def resetfunc():
        return random.randrange(0, disksize-bufsize)
    def func(offset):
        os.pread(disk.fileno(), bufsize, offset)
    times = timeit2(resetfunc, func)

    print('Buffer size: {:5}   Average: {}/sec   Samples: {}'.format(
        BytesString(bufsize), BytesStringFloat(bufsize/(sum(times)/len(times))).rjust(9), len(times), ))


#--------------------------------------------------------------------------------------------------

print()
print('Measuring: Sequential read throughput with various buffer sizes.')

for bs in ['1MB','2MB','4MB','8MB','16MB','32MB','64MB','128MB','256MB']:
    os.system('echo 3 | sudo tee /proc/sys/vm/drop_caches > /dev/null')
    
    bufsize = BytesInt(bs)
    bufindex = 0
    def resetfunc():
        global bufindex
        bufindex += 1
        return bufindex * bufsize
    def func(offset):
        os.pread(disk.fileno(), bufsize, offset)
    times = timeit2(resetfunc, func)

    print('Buffer size: {:5}   Average: {}/sec   Samples: {}'.format(
        BytesString(bufsize), BytesStringFloat(bufsize/(sum(times)/len(times))).rjust(9), len(times), ))


#--------------------------------------------------------------------------------------------------

os.system('echo mq-deadline | sudo tee /sys/block/%s/queue/scheduler > /dev/null' % dev)

print()
print('Returned disk scheduler to mq-deadline.')

