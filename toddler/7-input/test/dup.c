#include <unistd.h>
#include <stdio.h>
void main(){
    dup2(1,3);
    write(3,"123",3);
}
