#!/usr/bin/python3
import struct, pickle, os, ctypes

libc = ctypes.cdll.LoadLibrary("libc.so.6")

def fallocate(fd, mode, offset, length):
    libc.fallocate(ctypes.c_int(fd), ctypes.c_int(mode), ctypes.c_longlong(offset), ctypes.c_longlong(length))


class Container:
    """Key-value file based database. Item access can only be used for single key query and update so no slices. Provides len.

    Requires an *atomic ordered filesystem* to guarantee crash consistency. Database can get compacted by sparsing the file. No thread safety. No file locking or concurrency. Pickle module restrictions apply."""

    def __init__(self, filename):
        """Constructor. Opens a file holding database that is of required format or is empty. Changes need to be manually committed to disk."""
        try:
            self.file = open(filename, "r+b")
        except FileNotFoundError:
            self.file = open(filename, "x+b")
        self.revert()

    def __del__(self):
        self.file.close()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.file.close()

    def __getitem__(self, key):
        return self.get(key)

    def __setitem__(self, key, value):
        self.set(key, value)

    def __len__(self):
        return len(self.keys)

    def __contains__(self, key):
        return key in self.keys

    def __iter__(self):
        return self.keys

    def __repr__(self):
        return '<Container: file {0}>'.format(self.file.name)

    def get(self, key):
        """Returns the value for specified key. Throws KeyError if key was not found."""
        dumpat, dumplen = self.keys[key]
        self.file.seek(dumpat, 0)
        return pickle.loads(self.file.read(dumplen))

    def getkeys(self):
        """Returns a list of all keys."""
        return list(self.keys.keys())

    def set(self, key, value):
        """Assigns a value to new or existing key. Changes are not persisted until commited."""
        dump = pickle.dumps(value)
        dumpat = max(8, self.file.seek(0, 2))
        dumplen = len(dump)
        self.file.write(dump)
        self.keys[key] = (dumpat, dumplen)

    def setfrom(self, key, sourcekey)
        """Assigns existing value to another key. This uses less disk space than setting keys separately. Changes are not persisted until commited."""
        self.keys[key] = self.keys[sourcekey]

    def remove(self, key):
        """Removes a specified existing key-value. Throws KeyError if key not found. Reclaims disk space by sparsing the file. Changes are not persisted until commited."""
        punchat, punchlen = self.keys.pop(key)
        self.awaitingpunch.append((punchat, punchlen))

    def removeall(self):
        """Removes all key-values. Reclaims disk space by truncating the file. Changes are not persisted until commited."""
        for punchat, punchlen in self.keys.items():
            self.awaitingpunch.append((punchat, punchlen))
        self.keys = {}

    def commit(self):
        """Persists changes made to the database."""
        if self.keys:
            self.file.seek(0, 0)
            dump = self.file.read(8)
            if sum(dump):
                rootat, rootlen = struct.unpack("<LL", dump)
                self.awaitingpunch.append((rootat, rootlen))

            dump = pickle.dumps(self.keys)
            dumpat = max(8, self.file.seek(0, 2))
            dumplen = len(dump)
            self.file.write(dump)
            self.file.flush()
            os.fsync(self.file.fileno())
            self.file.seek(0, 0)
            self.file.write(struct.pack("<LL", dumpat, dumplen))
            self.file.flush()
            os.fsync(self.file.fileno())

            for punchat, punchlen in self.awaitingpunch.items():
                fallocate(self.file.fileno(), 3, punchat, punchlen)
            self.awaitingpunch.clear()
        else:
            self.file.truncate(0)
            self.awaitingpunch.clear()
            os.fsync(self.file.fileno())

    def revert(self):
        """Rolls back the changes made to the database since last commit."""
        self.file.seek(0, 0)
        dump = self.file.read(8)
        if sum(dump):
            rootat, rootlen = struct.unpack("<LL", dump)
            self.file.seek(rootat, 0)
            self.keys = pickle.loads(self.file.read(rootlen))
            self.awaitingpunch = []
        else:
            self.keys = {}
            self.awaitingpunch = []
