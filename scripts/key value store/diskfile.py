from io import BufferedRandom
import os


class DiskFile(BufferedRandom):

    def __init__(self, raw):
        super(DiskFile, self).__init__(raw)

    def readp(self, offset, length):
        return os.pread(self.fileno(), length, offset)

    def writep(self, offset, data):
        return os.pwrite(self.fileno(), data, offset)

    def sync(self):
        return os.fsync(self.fileno())

    def flushsync(self):
        self.flush()
        self.sync()
        return None #????

