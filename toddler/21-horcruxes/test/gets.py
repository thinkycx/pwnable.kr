#!/usr/bin/env python
# coding=utf-8
from pwn import *
p = process("./a.out")
print 'haha'
payload = "1334\t5\x006\n666"
p.sendlineafter("orld", payload)
p.interactive()
