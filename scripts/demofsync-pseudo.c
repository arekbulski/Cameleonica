int fd = creat("file.new", S_IRUSR|S_IWUSR);
write(fd, buf, 255);
fsync(fd);
close(fd);
int dirfd = open(".", O_DIRECTORY);
fsync(dirfd);
close(dirfd);
rename("file.new", "file");
