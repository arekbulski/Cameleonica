#!/usr/bin/python3
import struct, pickle, os
import diskfile


class Container:
    """Key-value file based simple database. Item access can only be used for single key query update and delete, or `...` to query or delete all items.

    Uses but not strictly requires an *atomic ordered filesystem* to guarantee consistency. Database can get smaller by punching holes in the file. No thread safety. No file locking. Pickle module restrictions apply. Should not be used for very large entries or very large amounts of entries. Changes are seekless (unless autocommit is turned on), and a commit needs at most 2 seeks. """

    # Following fields are used throughout the class code:
    # - keys: The main dictionary mapping.
    # - buffered: Those changed values were written into memory but not onto disk yet.
    # - cache: Those were read from disk and unpickled (or inserted) and cached for later.
    # - awaitingpunch: Those value blobs were removed or overwritten.

    def __init__(self, filename, overwrite=False, autocommit=False):
        """Constructor. Opens or creates a file holding the database. """
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
        else:
            return self.get(key)

    def __setitem__(self, key, value):
        self.set(key, value)

    def __delitem__(self, key):
        if key is Ellipsis:
            self.removeall()
        else:
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
        """Returns the value for a specified key. Throws KeyError if key was not found. May require at most 1 disk seek (unless it is already in the cache). """
        if key in self.cache:
            return self.cache[key]
        valueat,valuelen = self.keys[key]
        valuedump = self.file.readp(valueat, valuelen)
        value = pickle.loads(valuedump)
        self.cache[key] = value
        return value

    def getkeys(self):
        """Returns a list of all keys. Diskless. """
        return list(self.keys)

    def getitems(self):
        """Returns all keys and their values. May require many disk seeks. After this method, the cache contains all values. """
        return {k:self.get(k) for k in self.keys}

    def set(self, key, value):
        """Assigns a value to either a new or an existing key. Changes are not persisted until commited. """
        if key in self.keys:
            self.remove(key)
        self.keys[key] = None
        self.buffered[key] = value
        self.cache[key] = value
        if self.autocommit:
            commit()

    def remove(self, key):
        """Removes a specified existing key-value. If the key does not exist, nothing happens. Changes are not persisted until commited. """
        
        # If there used to be a key, there must exist an old value blob somewhere in the database. It should be deallocated after a successful commit to disk.
        if key in self.keys:
            if self.keys[key] is not None:
                punchat,punchlen = self.keys[key]
                self.awaitingpunch.append((punchat, punchlen))

        self.keys.pop(key, None)
        self.buffered.pop(key, None)
        self.cache.pop(key, None)

        if self.autocommit:
            commit()

    def removeall(self):
        """Removes all key-values. Changes are not persisted until commited. If the store gets commited immediately after all keys were removed, the file gets truncated to zero, otherwise all existing blobs get punched into holes. """

        # If there used to be a key, there must exist an old value blob somewhere in the database. It should be deallocated after a successful commit to disk.
        for key in self.keys:
            if self.keys[key] is not None:
                punchat,punchlen = self.keys[key]
                self.awaitingpunch.append((punchat, punchlen))
        
        self.keys = {}
        self.buffered = {}
        self.cache = {}
        
        if self.autocommit:
            commit()

    def commit(self):
        """Persists changes onto disk. If some keys were removed, holes are punched through. If all keys were removed, file is truncated. """
        if self.keys:
            # If there used to be some keys, there must exist an old dictionary blob somewhere in the database. It should be deallocated after a successful commit to disk.
            self.file.seek(0)
            headerdump = self.file.read(16)
            if sum(headerdump):
                dictat,dictlen = struct.unpack("<QQ", headerdump)
                self.awaitingpunch.append((dictat,dictlen))

            # All buffered (modified but uncommited) values get serialized and sent to disk.
            for key,value in self.buffered.items():
                valuedump = pickle.dumps(value)
                valueat = self.file.safeappend(valuedump, 16)
                self.keys[key] = (valueat,len(valuedump))
            self.buffered.clear()

            # A new dictionary blob gets serialized and sent to disk.
            dictdump = pickle.dumps(self.keys)
            dictat = self.file.safeappend(dictdump, 16)

            # Finally, the header gets overwritten atomically and orderly.
            headerdump = struct.pack("<QQ", dictat, len(dictdump))
            self.file.fsync()
            self.file.writep(0, headerdump)
            self.file.fsync()

            # Whatever value blobs and dictionary blobs are no longer being pointed to, they can be safely deallocated.
            for (punchat,punchlen) in self.awaitingpunch:
                self.file.fallocate(2|1, punchat, punchlen)
            self.awaitingpunch.clear()

            self.buffered.clear()

        else:
            self.awaitingpunch.clear()
            self.file.fsync()
            self.file.truncate(0)
            self.file.fsync()

    def revert(self):
        """Rolls back the changes made to the database since last commit. It can also be used by the class constructor to pre-load the header and dictionary. """
        headerdump = self.file.readp(0, 16)
        if sum(headerdump):
            dictat,dictlen = struct.unpack("<QQ", headerdump)
            dictblob = self.file.readp(dictat, dictlen)
            self.keys = pickle.loads(dictblob)
            self.buffered = {}
            self.cache = {}
            self.awaitingpunch = []

        else:
            self.keys = {}
            self.buffered = {}
            self.cache = {}
            self.awaitingpunch = []
