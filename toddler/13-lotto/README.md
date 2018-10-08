```c
lotto - 2 pt [writeup] 

Mommy! I made a lotto program for my homework.
do you want to play?


ssh lotto@pwnable.kr -p2222 (pw:guest)
```



`scp -P 2222 -p  lotto@pwnable.kr:/home/lotto/* ./`下载程序。

根据下载程序中的信息可知，这是一个韩国（kr）的nlotto彩票游戏，选六个数字，原始的中奖概率是1 / 8,145,060。http://www.nlotto.co.kr/counsel.do?method=playerGuide#buying_guide01



IDA pseudocode

```c
unsigned __int64 play()
{
  signed int i; // [rsp+Ch] [rbp-24h]
  signed int j; // [rsp+Ch] [rbp-24h]
  int v3; // [rsp+10h] [rbp-20h]
  signed int k; // [rsp+14h] [rbp-1Ch]
  int fd; // [rsp+1Ch] [rbp-14h]
  char buf[8]; // [rsp+20h] [rbp-10h]
  unsigned __int64 v7; // [rsp+28h] [rbp-8h]

  v7 = __readfsqword(0x28u);
  printf("Submit your 6 lotto bytes : ");
  fflush(stdout);
  read(0, submit, 6uLL);                        // user input
  puts("Lotto Start!");
  fd = open("/dev/urandom", 0);
  if ( fd == -1 )
  {
    puts("error. tell admin");
    exit(-1);
  }
  if ( (unsigned int)read(fd, buf, 6uLL) != 6 )
  {
    puts("error2. tell admin");
    exit(-1);
  }
  for ( i = 0; i <= 5; ++i )
    buf[i] = (unsigned __int8)buf[i] % 45u + 1; // 1-45
  close(fd);
  v3 = 0;
  for ( j = 0; j <= 5; ++j )
  {
    for ( k = 0; k <= 5; ++k )
    {
      if ( buf[j] == submit[k] )
        ++v3;
    }
  }
  if ( v3 == 6 )
    system("/bin/cat flag");
  else
    puts("bad luck...");
  return __readfsqword(0x28u) ^ v7;
}
```

主要的函数就是一个play，从STDIN read 6byte到submit数组（位于bss段），从/dev/urandom读6byte到buf数组（位于stack）中，buf中每个字符%45+1，范围（1-45）。然后判断一下buf和submit，相等就拿flag。

漏洞发生在判断相等的时候，判断了6*6 36次。因此，只要submit中有一位和buf数组中的一位相等，v3就等于6。概率大约是6/45（未排除多个数字重复的情况）。手工输入一个ascii（1-15）的字符6次即可。我输入的是空格（0x20）。

## flag

```
- Select Menu -
1. Play Lotto
2. Help
3. Exit
1
Submit your 6 lotto bytes :
Lotto Start!
bad luck...
- Select Menu -
1. Play Lotto
2. Help
3. Exit
1
Submit your 6 lotto bytes :
Lotto Start!
sorry mom... I FORGOT to check duplicate numbers... :(
```

