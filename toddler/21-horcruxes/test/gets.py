#!/usr/bin/env python
# coding=utf-8
from pwn import *
context.terminal = ['tmux', 'splitw', '-h' ]
p = process("./a.out")
gdb.attach(p)
print 'haha'
payload = "1\x00\x003\x006\n666"
p.sendlineafter("orld", payload)
p.interactive()
