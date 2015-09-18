#include <fcntl.h>
#include <stdio.h>
#include <assert.h>

int main()
{
	int fd = creat("file.new", S_IRUSR|S_IWUSR);
	printf("creat -> %d \n", fd);
	assert(fd >= 0);

	char buf[255];
	int err = write(fd, buf, 255);
	printf("write -> %d \n", err);
	assert(err == 255);

	err = fsync(fd);
	printf("fsync -> %d \n", err);
	assert(err == 0);

	err = close(fd);
	printf("close -> %d \n", err);
	assert(err == 0);

	int dirfd = open(".", O_DIRECTORY);
	printf("open on dir -> %d \n", dirfd);
	assert(dirfd >= 0);

	err = fsync(dirfd);
	printf("fsync on dir -> %d \n", err);
	assert(err == 0);

        err = close(dirfd);
        printf("close on dir -> %d \n", err);
        assert(err == 0);

	err = rename("file.new", "file");
	printf("rename -> %d \n", err);
	assert(err == 0);

	return 0;
}
