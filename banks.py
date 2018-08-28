from __future__ import print_function
from collections import defaultdict

class Dim3(object):
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __iter__(self):
        for z in range(self.z):
            for y in range(self.y):
                for x in range(self.x):
                    yield ThreadIdx(x,y,z)

class ThreadIdx(object):
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return "(" + str(self.x) + "," + str(self.y) + "," + str(self.z) + ")"

class Shared(object):
    def __init__(self, num_banks, bank_width):
        self.num_banks = num_banks
        self.bank_width = bank_width
        self.banks = [0 for i in range(num_banks)]

    def access(self, address):
        
        word = int(address / self.bank_width)
        bank = word % len(self.banks)
        print("addr:{}->word:{}->bank:{}".format(address, word, bank))
        self.banks[bank] += 1

class Pointer(object):
    def __init__(self, dsize):
        self.dsize = dsize
        self.offset = 0

    def address_of(self, i):
        return self.offset + self.dsize * i

# Block configuration
blockDim = Dim3(10, 10, 10)

# pointer to 4-byte type
p = Pointer(4)

# 32 banks, 4-byte bank size
cc70 = Shared(32, 4)




accesses = defaultdict(list)
for threadIdx in blockDim:
    address = p.address_of(threadIdx.y * blockDim.x + threadIdx.x)
    cc70.access(address)

print("bank_width:{}".format(cc70.bank_width))
print("num_banks:{}".format(cc70.num_banks))
print(cc70.banks)
