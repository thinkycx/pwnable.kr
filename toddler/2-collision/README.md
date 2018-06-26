## TARGET
```
collision - 3 pt [writeup] 

Daddy told me about cool MD5 hash collision today.
I wanna do something like that too!

ssh col@pwnable.kr -p2222 (pw:guest)
```

## WRITEUP
download:
`scp -P 2222 -p  col@pwnable.kr:/home/col/* ./`
程序获取length为20的argv[1]，使用check_password函数将argv[1]运算后，和hashcode (int)0x21DD09ECh比较，如果相等，拿到拿到flag。check_password中，将a1按照DWORD 4byte取5个signed int累加返回。因此，构造字符串argv[1]为五个signed int即可。hex(0x21dd09ec - 0x01010101*4)='0x1dd905e8'。

EXP: 
```
col@ubuntu:~$ ./col `python -c 'print "\x01"*16+"\xe8\x05\xd9\x1d"'`
daddy! I just managed to create a hash collision :)
```

IDA pseudocode:
```c
int __cdecl check_password(int a1)
{
  signed int i; // [esp+4h] [ebp-Ch]
  int v3; // [esp+8h] [ebp-8h]

  v3 = 0;
  for ( i = 0; i <= 4; ++i )
    v3 += *(_DWORD *)(a1 + 4 * i);
  return v3;
}
```

IDA disassemable:
```asm
.text:08048494 check_password  proc near               ; CODE XREF: main+92↓p
.text:08048494
.text:08048494 i               = dword ptr -0Ch
.text:08048494 result          = dword ptr -8
.text:08048494 var_4           = dword ptr -4
.text:08048494 arg_0           = dword ptr  8
.text:08048494
.text:08048494 ; __unwind {
.text:08048494                 push    ebp
.text:08048495                 mov     ebp, esp
.text:08048497                 sub     esp, 10h
.text:0804849A                 mov     eax, [ebp+arg_0]
.text:0804849D                 mov     [ebp+var_4], eax
.text:080484A0                 mov     [ebp+result], 0
.text:080484A7                 mov     [ebp+i], 0
.text:080484AE                 jmp     short for
.text:080484B0 ; ---------------------------------------------------------------------------
.text:080484B0
.text:080484B0 func:                                   ; CODE XREF: check_password+32↓j
.text:080484B0                 mov     eax, [ebp+i]
.text:080484B3                 shl     eax, 2          ; i  = i * 4
.text:080484B6                 add     eax, [ebp+var_4] ; ebp+var_4 = (char *)&argv[1]
.text:080484B9                 mov     eax, [eax]
.text:080484BB                 add     [ebp+result], eax
.text:080484BE                 add     [ebp+i], 1
.text:080484C2
.text:080484C2 for:                                    ; CODE XREF: check_password+1A↑j
.text:080484C2                 cmp     [ebp+i], 4
.text:080484C6                 jle     short func
.text:080484C8                 mov     eax, [ebp+result]
.text:080484CB                 leave
.text:080484CC                 retn
.text:080484CC ; } // starts at 8048494
.text:080484CC check_password  endp
```

## TIPS
argv作为二级指针传递给程序，保存了运行的参数信息。printf("usage : %s [passcode]\n", *argv);会输出argv[0]，直接运行程序argv[0]为./bof，gdb调试argv[0]包含了绝对路径/home/col/col。

