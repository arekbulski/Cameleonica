#!/usr/bin/python3
import struct, pickle, os
import diskfile


class Container:
    """Key-value file based database. Item access can only be used for single key query and update, or `...` to query all items.

    Requires an *atomic ordered filesystem* to guarantee crash consistency. Database can get compacted by sparsing or truncating the file. No thread safety. No file locking. Pickle module restrictions apply. Should not be used for large entries or large amounts of entries. Changes are seekless, and commit need 2 seeks. """

    def __init__(self, filename, overwrite=False, autocommit=False):
        """Constructor. Opens a file holding database that is of required binary read-write mode. """
        if overwrite:
            self.file = diskfile.open2(filename, "w+b")
        else:
            try:
                self.file = diskfile.open2(filename, "r+b")
            except FileNotFoundError:
                self.file = diskfile.open2(filename, "x+b")
        self.autocommit = autocommit
        self.revert()

    def __del__(self):
        self.file.close()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.file.close()

    def __getitem__(self, key):
        if key is Ellipsis:
            return self.getitems()
        return self.get(key)

    def __setitem__(self, key, value):
        self.set(key, value)

    def __delitem__(self, key):
        self.remove(key)

    def __len__(self):
        return len(self.keys)

    def __contains__(self, key):
        return key in self.keys

    def __iter__(self):
        return self.keys

    def __repr__(self):
        return '<Container: {0}>'.format(self.file.name)

    def get(self, key):
        """Returns the value for specified key. Throws KeyError if key was not found. """
        if key in self.cache:
            return self.cache[key]
        dumpat,dumplen = self.keys[key]
        value = pickle.loads(self.file.readp(dumpat, dumplen))
        self.cache[key] = value
        return value

    def getkeys(self):
        """Returns a list of all keys."""
        return list(self.keys)

    def getitems(self):
        """Returns all keys and their values. May require many disk seeks for many uncommited keys. """
        return {k:self.get(k) for k in self.keys}

    def set(self, key, value):
        """Assigns a value to new or existing key. Changes are not persisted until commited. """
        if key in self.keys:
            self.remove(key)
        self.keys[key] = None
        self.cache[key] = value
        if self.autocommit:
            commit()

    def remove(self, key):
        """Removes a specified existing key-value. Throws KeyError if key not found. Changes are not persisted until commited. """
        pointers = self.keys.pop(key)
        if pointers is not None:
            punchat,punchlen = pointers
            self.awaitingpunch.append((punchat, punchlen))
        if self.autocommit:
            commit()

    def removeall(self):
        """Removes all key-values. Changes are not persisted until commited."""
        for pointers in self.keys.values():
            if pointers is not None:
                punchat,punchlen = pointers
                self.awaitingpunch.append((punchat, punchlen))
        self.keys = {}
        if self.autocommit:
            commit()

    def commit(self):
        """Persists changes onto disk. If some keys were removed, holes are punched through. If all keys were removed, file is truncated. """
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

            for punchat,punchlen in self.awaitingpunch:
                self.file.fallocate(3, punchat, punchlen)
            self.awaitingpunch.clear()
        else:
            self.file.truncate(0)
            self.awaitingpunch.clear()
            os.fsync(self.file.fileno())

    def revert(self):
        """Rolls back the changes made to the database since last commit. Requires one disk seek. """
        dump = self.file.readp(0, 8)
        if sum(dump):
            rootat,rootlen = struct.unpack("<LL", dump)
            self.keys = pickle.loads(self.file.readp(rootat, rootlen))
            self.cache = {}
            self.awaitingpunch = []
        else:
            self.keys = {}
            self.cache = {}
            self.awaitingpunch = []
