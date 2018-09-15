import random
import math
import w3.config as conf
from helper.testutils import O

class Sample:
    def __init__(self, max=conf.SAMPLE['max'], txt=False):
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
            self.some[math.floor(int(random.random() * now))] = x
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


@O.k
def sampleTest():
    random.seed(1)
    s = []
    for idx in range(5, 10):
        s.append(Sample(max=2 ** idx))

    for idx in range(1, 10001):
        y = random.random()
        for t in s:
            t.sampleInc(y)

    for t in s:
        print(t.max, t.nth(0.5))


if __name__ == "__main__":
    O.report()
