## TASK
```
flag - 7 pt [writeup] 

Papa brought me a packed present! let's open it.

Download : http://pwnable.kr/bin/flag

This is reversing task. all you need is binary
```

## WRITEUP
IDA 分析源程序，发现字符串中有upx，upx -d解压后IDA继续后即可看见程序malloc一块内存只有，调用strcpy拷贝了flag。这题gdb动态调试也可以。
```
$ file flag
flag: ELF 64-bit LSB executable, x86-64, version 1 (GNU/Linux), statically linked, stripped
$ upx -d ./flag
                       Ultimate Packer for eXecutables
                          Copyright (C) 1996 - 2013
UPX 3.91        Markus Oberhumer, Laszlo Molnar & John Reiser   Sep 30th 2013

        File size         Ratio      Format      Name
   --------------------   ------   -----------   -----------
    887219 <-    335288   37.79%  linux/ElfAMD   flag

Unpacked 1 file.
$ file flag
flag: ELF 64-bit LSB executable, x86-64, version 1 (GNU/Linux), statically linked, for GNU/Linux 2.6.24, BuildID[sha1]=96ec4cc272aeb383bd9ed26c0d4ac0eb5db41b16, not stripped
```
IDA disassemble：
```
.text:0000000000401164 ; __unwind {
.text:0000000000401164                 push    rbp
.text:0000000000401165                 mov     rbp, rsp
.text:0000000000401168                 sub     rsp, 10h
.text:000000000040116C                 mov     edi, offset aIWillMallocAnd ; "I will malloc() and strcpy the flag the"...
.text:0000000000401171                 call    puts
.text:0000000000401176                 mov     edi, 64h
.text:000000000040117B                 call    malloc
.text:0000000000401180                 mov     [rbp+dest], rax
.text:0000000000401184                 mov     rdx, cs:flag
.text:000000000040118B                 mov     rax, [rbp+dest]
.text:000000000040118F                 mov     rsi, rdx        ; src
.text:0000000000401192                 mov     rdi, rax        ; dest
.text:0000000000401195                 call    _strcpy
.text:000000000040119A                 mov     eax, 0
.text:000000000040119F                 leave
.text:00000000004011A0                 retn
.text:00000000004011A0 ; } // starts at 401164
.text:00000000004011A0 main            endp

.data:00000000006C2070 flag            dq offset aUpxSoundsLikeA
.data:00000000006C2070                                         ; DATA XREF: main+20↑r
.data:00000000006C2070                                         ; "UPX...? sounds like a delivery service "...
```
## flag
UPX...? sounds like a delivery service :)
