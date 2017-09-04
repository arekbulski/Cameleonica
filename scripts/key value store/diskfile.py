#!/usr/bin/python3
import os, io, ctypes


libc = ctypes.cdll.LoadLibrary("libc.so.6")


class BufferedRandom2(io.BufferedRandom):

    def __init__(self, stream):
        super().__init__(stream)

    def readp(self, offset, length):
        return os.pread(self.fileno(), length, offset)

    def writep(self, offset, data):
        return os.pwrite(self.fileno(), data, offset)

    def sync(self):
        return os.fsync(self.fileno())

    def flushsync(self):
        self.flush()
        self.sync()

    def fallocate(self, mode, offset, length):
        libc.fallocate(ctypes.c_int(self.fileno()), ctypes.c_int(mode), ctypes.c_longlong(offset), ctypes.c_longlong(length))


def open2(filename, mode):
    return BufferedRandom2(open(filename, mode))
