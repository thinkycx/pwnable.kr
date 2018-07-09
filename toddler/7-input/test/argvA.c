#include <stdio.h>
void main(int argc,char **argv,char **env){
    for(int i=0;i<argc;i++){
        printf("%d \n", i);
        printf("%s - HEX: ",argv[i]);
        char *a, b ;
        a = argv[i];
        while(b = *(char *)a){
            printf("%x ",b);
            a++;
        }
        printf("\n");
        
    }
    printf("argv['A']: %s\n",argv['A']);
}
