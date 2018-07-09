#include <unistd.h>
void main(){
    char *argv[101]={"/tmp/input2",[1 ... 99]="A",NULL};
    argv['A'] = "\x00";
    argv['B'] = "\x20\x0a\x0d";
    execve(argv[0],argv,NULL);
}
