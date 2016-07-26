#!/usr/bin/python3
import struct, pickle, os

class Container:
    """Key-value file based database. Requires an *atomic ordered filesystem* to guarantee crash consistency. Currently database never shrinks. No thread safety. No file locking or concurrency. Pickle module restrictions apply."""

    def __init__(self, filename, *, autocommit=False):
        """Constructor. Opens a file holding database that is of required format or is empty. By default, changes need to be manually committed to disk."""
        try:
            self.file = open(filename, "r+b")
        except FileNotFoundError:
            self.file = open(filename, "w+b")
        self.autocommit = autocommit
        self.revert()

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
        self.internalautocommit()

    def setfrom(self, key, sourcekey)
        """Assigns existing value to another key. This uses less disk space than setting keys separately. Changes are not persisted until commited."""
        self.keys[key] = self.keys[sourcekey]
        self.internalautocommit()

    def remove(self, key):
        """Removes a specified existing key-value. Throws KeyError if key not found. Does not reclaim disk space yet. Changes are not persisted until commited."""
        self.keys.pop(key)
        self.internalautocommit()

    def removeall(self):
        """Removes all key-values. Reclaims entire disk space. Changes are not persisted until commited."""
        self.keys = {}
        self.internalautocommit()

    def commit(self):
        """Persists changes made to the database."""
        if self.keys:
            dump = pickle.dumps(self.keys)
            dumpat = max(8, self.file.seek(0, 2))
            dumplen = len(dump)
            self.file.write(dump)
            self.file.seek(0, 0)
            self.file.write(struct.pack("<LL", dumpat, dumplen))
        else:
            self.file.seek(0, 0)
            self.file.truncate()

    def internalautocommit():
        """Used internally."""
        if self.autocommit:
            self.commit()

    def revert(self):
        """Rolls back the changes made to the database since last commit."""
        self.file.seek(0, 0)
        dump = self.file.read(8)
        if sum(dump):
            rootat, rootlen = struct.unpack("<LL", dump)
            self.file.seek(rootat, 0)
            self.keys = pickle.loads(self.file.read(rootlen))
        else:
            self.keys = {}
