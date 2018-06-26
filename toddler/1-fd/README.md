## TARGET
```
fd - 1 pt [writeup] 

Mommy! what is a file descriptor in Linux?

* try to play the wargame your self but if you are ABSOLUTE beginner, follow this tutorial link:
https://youtu.be/971eZhMHQQw

ssh fd@pwnable.kr -p2222 (pw:guest)
"""
```
## WRITEUP
download:
`scp -P 2222 -p  fd@pwnable.kr:/home/fd/* ./`

IDA pseudocode:
```c
 if ( argc > 1 )
  {
    v4 = atoi(argv[1]);
    read(v4 - 4660, &buf, 0x20u);
    v7 = 10;
    v8 = "LETMEWIN\n";
    v9 = &buf;
    do
    {
      if ( !v7 )
        break;
      v5 = (const unsigned __int8)*v8 < *v9;
      v6 = *v8++ == *v9++;
      --v7;
    }
    while ( v6 );
    if ( (!v5 && !v6) == v5 )                   // v6 == 1, v5 == 0
    {
      puts("good job :)");
      system("/bin/cat flag");
      exit(0);
    }
    puts("learn about Linux file IO");
    result = 0;
  }
  else
  {
    puts("pass argv[1] a number");
    result = 0;
  }
```
程序调用read函数从fd = atoi(argv[1]) - 4660读，之后和"LETMEWIN\n"按照字节比10次。  
如果想进入system流程，let v6 == 1 and v5 == 0.因此，从fd读取的字符串和"LETMEWIN\n"相等即可。  
PS: 对比源码，strcmp参数之一是静态字符串，所以可能做了编译优化，变成了按字节比较。

EXP:
```
fd@ubuntu:~$ echo "LETMEWIN" | ./fd 4660
good job :)
mommy! I think I know what a file descriptor is!!
```