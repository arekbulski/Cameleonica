#!/usr/bin/env python

import os, sys, errno
from fuse import FUSE, FuseOSError, Operations
import Pyro4
from base64 import b64encode, b64decode


class Passthrough(object):
    def __init__(self):
        pass

    def setroot(self, root):
        self.root = root

    def fullpath(self, partial):
        return os.path.join(self.root, partial.lstrip('/'))

    def access(self, path, mode):
        return os.access(self.fullpath(path), mode)

    def chmod(self, path, mode):
        return os.chmod(self.fullpath(path), mode)

    def chown(self, path, uid, gid):
        return os.chown(self.fullpath(path), uid, gid)

    def getattr(self, path, fh=None):
        st = os.lstat(self.fullpath(path))
        return dict((key, getattr(st, key)) for key in ('st_atime', 'st_ctime', 'st_gid', 'st_mode', 'st_mtime', 'st_nlink', 'st_size', 'st_uid'))

    def readdir(self, path, fh):
        return ['.','..'] + os.listdir(self.fullpath(path))

    def readlink(self, path):
        target = os.readlink(self.fullpath(path))
        if target.startswith('/'):
            # Path name is absolute, sanitize it.
            return os.path.relpath(target, self.root)
        else:
            return pathname

    def mknod(self, path, mode, dev):
        return os.mknod(self.fullpath(path), mode, dev)

    def rmdir(self, path):
        return os.rmdir(self.fullpath(path))

    def mkdir(self, path, mode):
        return os.mkdir(self.fullpath(path), mode)

    def statfs(self, path):
        stv = os.statvfs(self.fullpath(path))
        return dict((key, getattr(stv, key)) for key in ('f_bavail', 'f_bfree', 'f_blocks', 'f_bsize', 'f_favail', 'f_ffree', 'f_files', 'f_flag', 'f_frsize', 'f_namemax'))

    def unlink(self, path):
        return os.unlink(self.fullpath(path))

    def symlink(self, target, path):
        return os.symlink(target, self.fullpath(path))

    def rename(self, old, new):
        return os.rename(self.fullpath(old), self.fullpath(new))

    def link(self, target, path):
        return os.link(self.fullpath(target), self.fullpath(path))

    def utimens(self, path, times=None):
        return os.utime(self.fullpath(path), times)

    def open(self, path, flags):
        return os.open(self.fullpath(path), flags)

    def create(self, path, mode, fi=None):
        return os.open(self.fullpath(path), os.O_WRONLY | os.O_CREAT, mode)

    def read(self, path, length, offset, fh):
        os.lseek(fh, offset, os.SEEK_SET)
        return b64encode(os.read(fh, length))

    def write(self, path, buf, offset, fh):
        os.lseek(fh, offset, os.SEEK_SET)
        return os.write(fh, b64decode(buf))

    def truncate(self, path, length, fh=None):
        with open(self.fullpath(path), 'r+') as f:
            f.truncate(length)

    def flush(self, path, fh):
        return os.fsync(fh)

    def fsync(self, path, fdatasync, fh):
        return os.fsync(fh)

    def release(self, path, fh):
        return os.close(fh)


Pyro4.Daemon.serveSimple({ Passthrough():'fs' })
