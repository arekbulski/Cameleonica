#!/usr/bin/python2

import os, sys, errno
from fuse import FUSE, FuseOSError, Operations


class ThinFilesystem(Operations):
    # def __init__(self, fs):

    # def chmod(self, path, mode):
    # def chown(self, path, uid, gid):
    # def readlink(self, path):
    # def mknod(self, path, mode, dev):
    # def rmdir(self, path):
    # def mkdir(self, path, mode):
    # def unlink(self, path):
    # def symlink(self, target, path):
    # def rename(self, old, new):
    # def link(self, target, path):
    # def utimens(self, path, times=None):
    # def create(self, path, mode, fi=None):
    # def truncate(self, path, length, fh=None):
    # def fsync(self, path, fdatasync, fh):

    def access(self, path, mode):
        return True

    def getattr(self, path, fh=None):
        # return dict(st_mode=33261, st_nlink=1, st_uid=1000, st_gid=1000, st_size=1024**3)
        return dict(st_mode=33261, st_ino=51773573, st_dev=64768, st_nlink=1, st_uid=1000, st_gid=1000, st_size=58, st_atime=1504736212, st_mtime=1504736188, st_ctime=1504736188)

    def readdir(self, path, fh):
        return ['.','..','file1']

    def statfs(self, path):
        return dict(f_bsize=4096, f_frsize=4096, f_blocks=282316110, f_bfree=18082327, f_bavail=3724004, f_files=71778304, f_ffree=71751892, f_favail=71751892, f_flag=4102, f_namemax=255)

    #     return self.fs.statfs(path)

    def open(self, path, flags):
        return 101

    def read(self, path, length, offset, fh):
        return bytes(length)

    # def write(self, path, buf, offset, fh):
    #     return self.fs.write(path, b64encode(buf), offset, fh)

    # def flush(self, path, fh):
    #     return self.fs.flush(path, fh)

    def release(self, path, fh):
        pass

FUSE(ThinFilesystem(), sys.argv[1], nothreads=True, foreground=True)
