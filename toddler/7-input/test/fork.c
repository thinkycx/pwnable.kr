#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
void main(){
    pid_t pid;
    int pipefd[2];
    int n;
    char buf[100]={0};
    if(pipe(pipefd)<0 ){
        exit(-1);
    }
    pid = fork();
    if(pid == -1){
        printf("fork error");
        return;
    }else if(pid >0){
        close(pipefd[0]);
        write(pipefd[1],"pipe success\n",13);
 //       wait(NULL);
        
    }else if(pid==0){
        close(pipefd[1]);
        dup2(pipefd[0],0); //pipefd[0]  and  0

        n = read(0,buf,13);
        write(1, buf, n);
    }
}
