#!/usr/bin/python3
import os, io


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


def open2(filename, mode):
    return BufferedRandom2(open(filename, mode))
