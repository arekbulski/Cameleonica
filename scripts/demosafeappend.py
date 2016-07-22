#!/usr/bin/python3
import struct, pickle, os

class Container:

    def __init__(self, filename):
        try:
            self.file = open(filename, "r+b")
        except FileNotFoundError:
            self.file = open(filename, "w+b")
        self.revert()

    def get(self, key):
        if key not in self.keys:
            return None
        dumpat, dumplen = self.keys[key]
        self.file.seek(dumpat, 0)
        return pickle.loads(self.file.read(dumplen))

    def getkeys(self):
        return list(self.keys.keys())

    def set(self, key, value):
        dump = pickle.dumps(value)
        dumpat = self.file.seek(0, 2)
        dumplen = len(dump)
        self.file.write(dump)
        self.keys[key] = (dumpat, dumplen)

    def clear(self):
        self.keys = {}

    def commit(self):
        dump = pickle.dumps(self.keys)
        dumpat = self.file.seek(0, 2)
        dumplen = len(dump)
        self.file.write(dump)
        self.file.seek(0, 0)
        self.file.write(struct.pack("<LL", dumpat, dumplen))

    def revert(self):
        if self.file.seek(0, 2) == 0:
            self.file.seek(0, 0)
            self.file.write(bytes(8))
            self.keys = {}
            print('empty file')
        else:
            self.file.seek(0, 0)
            dump = self.file.read(8)
            rootat, rootlen = struct.unpack("<LL", dump)
            if rootlen > 0:
                self.file.seek(rootat, 0)
                self.keys = pickle.loads(self.file.read(rootlen))
                print("loaded root",self.keys,"at",rootat,"of",rootlen)
            else:
                self.keys = {}
                print('no root to load')

