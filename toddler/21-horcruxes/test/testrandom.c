#include <stdio.h>

int main()
{
    printf("Hello world\n");
    int fd=open("/dev/urandom", 0);
    char buf[4];
    read(fd, buf, 4);
    srand((int)buf);
    printf("%d\n", rand());
    printf("%d\n", rand());
    printf("%d\n", rand());
    printf("%d\n", rand());
    return 0;
}

