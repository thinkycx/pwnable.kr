#include <stdio.h>

int main()
{
    char buf[100];
    printf("Hello world\n", buf);
    gets(buf);
    printf("%s", buf);
    return 0;
}

