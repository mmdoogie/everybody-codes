from functools import total_ordering
from math import ceil

@total_ordering
class Bitvector:
    def __init__(self, max_bit, iv=0):
        self.max_bit = ceil((max_bit + 1) / 8) * 8 - 1
        self.data = bytearray((self.max_bit + 1) // 8)
        if iv != 0:
            for i, b in enumerate(reversed(bin(iv)[2:])):
                if b == '1':
                    self.__setitem__(i, b)

    def __getitem__(self, bit):
        if bit < 0 or bit > self.max_bit:
            raise IndexError(f'bit index out of range 0 to {self.max_bit}')
        return self.data[bit // 8] >> (bit % 8) & 0x01

    def __setitem__(self, bit, val):
        if bit < 0 or bit > self.max_bit:
            raise IndexError(f'bit index out of range 0 to {self.max_bit}')
        if val:
            self.data[bit // 8] |= 1 << (bit % 8)
        else:
            self.data[bit // 8] &= ~(1 << (bit % 8))

    def as_int(self):
        return int.from_bytes(self.data, byteorder='little')

    def bits(self):
        return [x for x in range(self.max_bit) if self.__getitem__(x)]

    def without(self, bit):
        self.__setitem__(bit, 0)
        return self

    def with_(self, bit):
        self.__setitem__(bit, 1)
        return self

    def __repr__(self):
        return 'bitvect<' + bin(self.as_int()) + '>'

    def __lt__(self, oth):
        if not isinstance(oth, Bitvector):
            return NotImplemented
        return self.as_int() < oth.as_int()

    def __eq__(self, oth):
        if not isinstance(oth, Bitvector):
            return NotImplemented
        return self.as_int() == oth.as_int()

    def __hash__(self):
        return self.as_int()

    @staticmethod
    def from_bits(max_bit, bit_list):
        v = Bitvector(max_bit)
        for b in bit_list:
            v[b] = True
        return v
