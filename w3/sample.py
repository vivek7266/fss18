import random
import math
from testutils import O

class Sample:
    def __init__(self, max=512, txt=False):
        self.max = max
        self.rank = 1
        self.txt = txt
        self.n = 0
        self.sorted = False
        self.some = []

    def sampleInc(self, x):
        self.n = self.n + 1
        now = len(self.some)
        if now < self.max:
            self.sorted = False
            self.some.append(x)
        elif random.random() < now / self.n:
            self.sorted = False
            self.some[math.floor(0.5 + random.random() * now)] = x
        return x

    def sampleSorted(self):
        if not self.sorted:
            self.some.sort()
            self.sorted = True
        return self.some

    def nth(self, n):
        s = self.sampleSorted()
        return s[min(len(s), max(1, math.floor(0.5 + len(s) * n)))]

    def nths(self):
        ns = [0.1, 0.3, 0.5, 0.7, 0.9]
        out = []
        for _, n in enumerate(ns):
            out.append(self.nth(n))
        return out

    # def sampleLt(self, s1, s2):
    #     return self.nth(s1, 0.5) < self.nth(s2, 0.5)
