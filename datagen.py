import random
import numpy as np
import uuid
import socket
import struct
import time
import numpy.random

def uniform_input_gen(n,m):
    f = open('uniform_input.txt','w')
    for i in range(n):
        l = random.randint(0,m-1)
        f.write(str(l)+'\n')
    f.close()

def exp_input_gen(n,m):
    p = []
    for i in range(m):
        p.append(1/(2**(i+1)))
    p = p/np.sum(p)
    f = open('exp_input.txt','w')
    for i in range(n):
        l = np.random.choice(m,p=p)
        f.write(str(l)+'\n')
    f.close()

def uuid_gen(n):
    f = open('uuid.txt','w')
    for i in range(n):
        id = uuid.uuid4()
        f.write(str(id)+'\n')
    f.close()

def ip_gen(n):
    f = open('ip.txt','w')
    for i in range(n):
        ip = socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff)))
        f.write(ip+'\n')
    f.close()

def ip_stream_gen(f,n,d,t):
    for i in range(d):
        t_i = t - d/2 + i
        if i < d/2:
            num_gen = int(n * 2 ** (-d/2+i))
        else:
            num_gen = int(n * 2 ** (d/2-i))
        for j in range(num_gen):
            ip = socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff)))
            f.write(str(t_i)+' '+ip+'\n')

def ip_stream_gen_1(n,d):
    f = open('ip_stream_3.txt','w')
    t = int(time.time())
    ip_stream_gen(f,n,d,t)

# uniform
def ip_stream_gen_2(n,d):
    f = open('ip_stream_2.txt','w')
    t = int(time.time())
    num_gen = int(n/d)
    for i in range(d):
        t_i = t - d / 2 + i
        for j in range(num_gen):
            ip = socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff)))
            f.write(str(t_i)+' '+ip+'\n')

