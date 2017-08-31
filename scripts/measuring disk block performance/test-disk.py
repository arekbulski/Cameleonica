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

def timeit(func, resetfunc=None, expectedtotal=5):
    total = 0
    times = []
    while True:
        if resetfunc is not None:
            resetfunc()
        t1 = time.perf_counter()
        func()
        t2 = time.perf_counter()
        times.append(t2-t1)
        total += t2-t1
        if total >= expectedtotal:
            return times

def timeit2(prefunc, func, expectedtotal=5):
    total = 0
    times = []
    while True:
        t1 = time.perf_counter()
        x = prefunc()
        t2 = time.perf_counter()
        func(x)
        t3 = time.perf_counter()
        times.append(t3-t2)
        total += t3-t1
        if total >= expectedtotal:
            return times


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
print('Disk name: {0}  Disk size: {1}  Scheduler disabled.'.format(disk.name, BytesStringFloat(disksize)))


#--------------------------------------------------------------------------------------------------

print()
print('Measuring: Track buffer working forward.')

for bufsize in [512*2**i for i in range(0,16)]:
    os.system('echo 3 | sudo tee /proc/sys/vm/drop_caches > /dev/null')

    def f():
        offset = random.randint(0, disksize-512-bufsize)
        os.pread(disk.fileno(), 512, offset)
        return offset
    def f2(offset):
        os.pread(disk.fileno(), bufsize, offset+512)
    times = timeit2(f, f2)

    print('Size tested: {:6}   Average: {:6.2f} ms   Max: {:6.2f} ms'.format(
        BytesString(bufsize), sum(times)/len(times)*1000, max(times)*1000 ))


#--------------------------------------------------------------------------------------------------

print()
print('Measuring: Track buffer working backwards.')

for bufsize in [512*2**i for i in range(0,16)]:
    os.system('echo 3 | sudo tee /proc/sys/vm/drop_caches > /dev/null')

    def f():
        offset = random.randint(0, disksize-512)
        os.pread(disk.fileno(), 512, offset)
        return offset
    def f2(offset):
        os.pread(disk.fileno(), bufsize, offset-bufsize)
    times = timeit2(f, f2)

    print('Size tested: {:6}   Average: {:6.2f} ms   Max: {:6.2f} ms'.format(
        BytesString(bufsize), sum(times)/len(times)*1000, max(times)*1000 ))


#--------------------------------------------------------------------------------------------------

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

print()
print('Measuring: Random seek time using beginning of disk.')

for area in [BytesInt('1MB')*2**i for i in range(0,64)]+[disksize]:
    if area > disksize:
        continue

    bufsize = 512
    os.system('echo 3 | sudo tee /proc/sys/vm/drop_caches > /dev/null')
    os.pread(disk.fileno(), bufsize, 0)
    times = timeit(lambda: os.pread(disk.fileno(), bufsize, random.randint(0, area-bufsize)))

    print('Area tested: {:6}   Average: {:5.2f} ms   Min: {:5.2f} ms   Max: {:5.2f} ms'.format(
        BytesString(area) if area < disksize else BytesStringFloat(area),
        sum(times)/len(times)*1000, min(times)*1000, max(times)*1000))


#--------------------------------------------------------------------------------------------------

print()
print('Measuring: Random read throughput with various sizes.')

for i in range(8):
    bufsize = BytesInt('1MB')*2**i
    times = timeit(lambda: os.pread(disk.fileno(), bufsize, random.randint(0, disksize-bufsize)),
                   lambda: os.system('echo 3 | sudo tee /proc/sys/vm/drop_caches > /dev/null') )

    print('Buffer: {:5}   Average: {:0.2f}sec   Average: {}/sec   Samples: {}'.format(
        BytesString(bufsize), sum(times)/len(times), BytesStringFloat(bufsize/(sum(times)/len(times))).rjust(9), len(times), ))


#--------------------------------------------------------------------------------------------------

print()
print('Measuring: Sequential read throughput using beginning of disk.')

bufsize = BytesInt('16MB')
disk.seek(0)
times = timeit(lambda: disk.read(bufsize),
               lambda: os.system('echo 3 | sudo tee /proc/sys/vm/drop_caches > /dev/null') )

print('Buffer: {:5}   Average: {:0.2f} sec   Average: {}/sec   Samples: {}'.format(
    BytesString(bufsize), sum(times)/len(times), BytesStringFloat(bufsize/(sum(times)/len(times))).rjust(9), len(times), ))


#--------------------------------------------------------------------------------------------------

os.system('echo cfq | sudo tee /sys/block/%s/queue/scheduler > /dev/null' % dev)

print()
print('Returned disk scheduler to CFQ.')
