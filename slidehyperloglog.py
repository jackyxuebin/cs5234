import math
from hashlib import sha256
from hashlib import md5
import mmh3
import fnv
from cityhash import CityHash32

def exact_streaming_map(fname):
    f = open(fname,'r')
    time_item_cnt = {}
    item_cnt = {}
    for l in f:
        t, w = l.split()
        if w not in item_cnt:
            item_cnt[w]=1
            time_item_cnt[(t,w)]=1
    return time_item_cnt

def exact_streaming_count(item_map,window,curr_t):
    c = 0
    for k,v in item_map.items():
        if  float(curr_t) - window  < float(k[0]) < curr_t:
            c+=1
    return c

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


class SlideHyperLogLog:
    def __init__(self, epsilon, hash, window):
        self.epsilon = epsilon
        self.hash = hash
        self.W = window
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
        self.M = [[] for i in range(self.m)]


    def add(self, value):
        t = float(value[0])
        v = value[1]
        x = self.hash(v)
        j = x & (self.m-1)
        w = x >> self.b
        #self.M[j] = max(self.M[j], 32 - self.b - w.bit_length() + 1)
        lpfm = self.M[j]
        # delete packets more than W seconds ago and packets with less maxima than current packet
        remove_list = []
        r = 32 - self.b - w.bit_length() + 1
        for p in lpfm:
            if float(p[0]) < t - self.W:
                remove_list.append(p)
            elif p[1] < r:
                remove_list.append(p)
        for p in remove_list:
            lpfm.remove(p)
        # add current packet
        lpfm.append((t,r))

    def card(self,w,t):
        #E = self.alpha * self.m**2 / sum(math.pow(2.0, -x) for x in self.M)
        # extract max R for each bucket in window w
        M = []
        for lpfm in self.M:
            lpfm_w = [p[1] for p in lpfm if  float(t)-w < float(p[0])]
            M.append(0 if len(lpfm_w)==0 else max(lpfm_w))
        E = self.alpha * self.m ** 2 / sum(math.pow(2.0, -x) for x in M)
        if E <= 5/2*self.m:
            V = M.count(0)
            if (V > 0):
                 E = self.m * math.log(self.m/V)
        elif E > 1/30 *2**32:
             E = -2**32*math.log(1-E/2**32)
        return E
