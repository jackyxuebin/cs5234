import math
from hashlib import sha256
from hashlib import md5
import mmh3
import fnv
from cityhash import CityHash32

def exact_count(fname):
    f = open(fname,'r')
    cnt = {}
    for l in f:
        ls = l.split()
        for w in ls:
            if w not in cnt:
                cnt[w]=1
    return len(cnt)

def hash_mmh3(x):
    return int(mmh3.hash(x,signed=False))

def hash_sha256(x):
    return int(sha256(x.encode('utf8')).hexdigest()[:8],16)

def hash_md5(x):
    return int(md5(x.encode('utf8')).hexdigest()[:8],16)

def hash_fnv(x):
    return fnv.hash(x.encode('utf8'),bits=32)

def hash_citi(x):
    return int(CityHash32(x.encode('utf8')))


class HyperLogLog:
    def __init__(self, epsilon, hash):
        self.epsilon = epsilon
        self.hash = hash
        if epsilon <= 0 or epsilon >= 1:
            raise ValueError('epsilon must be between 0 and 1')
        # b - length of bucket bitmap
        b = int(math.ceil(math.log((1.04 / epsilon) ** 2, 2)))
        if not (4 <= b <= 16):
            raise ValueError("L=%d should be in range [4 : 16]" % L)
        if b == 4:
            self.alpha = 0.673
        if b == 5:
            self.alpha = 0.697
        if b == 6:
            self.alpha = 0.709
        else:
            self.alpha = 0.7213 / (1.0 + 1.079 / (1 << b))
        self.b = b
        self.m = 1 << b
        self.M = [0 for i in range(self.m)]


    def add(self, value):
        x = self.hash(value)
        j = x & (self.m-1)
        w = x >> self.b
        self.M[j] = max(self.M[j], 32 - self.b - w.bit_length() + 1)

    def card(self):
        E = self.alpha * self.m**2 / sum(math.pow(2.0, -x) for x in self.M)
        if E <= 5/2*self.m:
            V = self.M.count(0)
            if (V > 0):
                 E = self.m * math.log(self.m/V)
        elif E > 1/30 *2**32:
             E = -2**32*math.log(1-E/2**32)
        return E
