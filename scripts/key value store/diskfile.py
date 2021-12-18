#!/usr/bin/python3
import os, io, ctypes


# This is used to effectuate the fallocate syscall.
libc = ctypes.cdll.LoadLibrary("libc.so.6")


# This is used when appending data to a file in a way where individual buffers are not crossing the 512 byte sector boundary.
def roundup(numerator, denominator):
    return ((numerator + denominator -1) // denominator) * denominator

# This is used when completing an append up to a sector boundary, so that there is no read-modify-write needed.
def remainder(numerator, denominator):
    return (-numerator) % denominator


class BufferedRandom2(io.BufferedRandom):

    def __init__(self, stream):
        """Opens the buffered file out of a given file steam."""
        super().__init__(stream)

    def readp(self, offset, length):
        """Reads the file at a given location."""
        return os.pread(self.fileno(), length, offset)

    def writep(self, offset, data):
        """Writes the file at a given location."""
        return os.pwrite(self.fileno(), data, offset)

    def safeappend(self, data, skip):
        """Writes the given data safely by appending, but (1) not before the skipped amount which is probably some header and (2) not across sector boundary. """
        minoffset = max(skip, self.seek(0, 2))
        offset = roundup(minoffset, 512)
        self.seek(offset)
        self.write(data)
        padding = bytes(remainder(len(data), 512))
        self.write(padding)
        return offset

    def fsync(self):
        """Flushes and syncs all data and metadata."""
        self.flush()
        return os.fsync(self.fileno())

    def fallocate(self, mode, offset, length):
        """Makes a selected fallocate (mode) operation on the file.
        - Mode 1 means to keep the size unchanged.
        - Mode 2 means to punch a hole (must be ORed with mode 1).
        - Mode 8 means to collapse a range.
        - Mode 16 means to zero a range.
        - Mode 32 means to insert a range.
        - Mode 64 means to unshare a range.
        """
        return libc.fallocate(ctypes.c_int(self.fileno()), ctypes.c_int(mode), ctypes.c_longlong(offset), ctypes.c_longlong(length)) == 0


def open2(filename, mode):
    return BufferedRandom2(open(filename, mode))
