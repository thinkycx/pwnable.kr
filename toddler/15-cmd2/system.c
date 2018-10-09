#include<stdio.h>
#include<stdlib.h>
void main(int argc, char **argv){
    if(argc<2){
        printf("./system COMMAND ");
    }
    printf("[*] debug system source code\n");
    printf("[*] COMMAND: %s \n", argv[1]);
    system(argv[1]);
}
