#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <string.h>
#include <arpa/inet.h>

void main(){
    char *argv[101]={"/home/input2/input",[1 ... 99]="A", NULL};
    argv['A'] = "\x00";
    argv['B'] = "\x20\x0a\x0d";
    argv['C'] = "7777";

    //stage 3
    char *env[2] = {"\xDE\xAD\xBE\xEF=\xCA\xFE\xBA\xBE", NULL};

    //stage 4
    FILE *fp = fopen("\x0a", "wb");
	if (fp == NULL) {
		perror("Open file recfile");
		exit(-1);
	}
    char *data = "\x00\x00\x00\x00";
    fwrite(data, sizeof(char), 4, fp);
    fclose(fp);

    //stage2    
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
    //  wait(NULL);
    
    // stage 5
    sleep(1);
    struct sockaddr_in servaddr;
	int sockfd;
	char *str = "\xde\xad\xbe\xef";

	sockfd = socket(AF_INET, SOCK_STREAM, 0);
	bzero(&servaddr, sizeof(servaddr));
	servaddr.sin_family = AF_INET;
	inet_pton(AF_INET, "127.0.0.1", &servaddr.sin_addr);
	servaddr.sin_port = htons(atoi(argv['C']));

	connect(sockfd, (struct sockaddr *)&servaddr, sizeof(servaddr));
	write(sockfd, str, strlen(str));
	close(sockfd);
        
    }else if(pid==0){
        close(pipefd1[1]);
        close(pipefd2[1]);

        dup2(pipefd1[0],0); //pipefd1[0]  and  0
        dup2(pipefd2[0],2); //pipefd2[0]  and  2

        //n = read(0,buf,13);
        //write(1, buf, n);

        execve(argv[0],argv, env);
    }


}
