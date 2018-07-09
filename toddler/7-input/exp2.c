#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>
void main(int argc, char **argv, char **env){
    char *arg[101]={"/tmp/input2",[1 ... 99]="A", NULL};
    arg['A'] = "\x00";
    arg['B'] = "\x20\x0a\x0d";
    
    pid_t pid;
    int pipefd1[2], pipefd2[2];
    //int n;
    //char buf[100]={0};
    if(pipe(pipefd1)<0 || pipe(pipefd2)<0){
        exit(-1);
    }
    pid = fork();
    if(pid == -1){
        printf("fork error");
        return;
    }else if(pid >0){
        close(pipefd1[0]);
        close(pipefd2[0]);
        write(pipefd1[1],"\x00\x0a\x00\xff",4);
        write(pipefd2[1],"\x00\x0a\x02\xff",4);
 //       wait(NULL);
        
    }else if(pid==0){
        close(pipefd1[1]);
        close(pipefd2[1]);

        dup2(pipefd1[0],0); //pipefd1[0]  and  0
        dup2(pipefd2[0],2); //pipefd2[0]  and  2

        //n = read(0,buf,13);
        //write(1, buf, n);

        execve(arg[0],arg,NULL);
    }


}
