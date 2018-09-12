from w3.sample import Sample


class Num:
    def __init__(self, max):
        self.n = 0
        self.mu = 0
        self.m2 = 0
        self.sd = 0
        self.lo = 10 ** 32
        self.hi = 10 ** -32
        self.some = Sample(max)
        self.w = 1

    def numInc(self, x):
        if x is None:
            return x
        self.n = self.n + 1
        self.some.sampleInc(x)
        d = x - self.mu
        self.mu = self.mu + d / self.n
        self.m2 = self.m2 + d * (x - self.mu)
        if x > self.hi:
            self.hi = x
        if x < self.lo:
            self.lo = x
        if self.n >= 2:
            self.sd = (self.m2 / (self.n - 1 + 10 ** -32)) ** 0.5
        return x

    def numDec(self, x):
        if x is None or self.n == 1:
            return x
        self.n = self.n - 1
        d = x - self.mu
        self.mu = self.mu - d / self.n
        self.m2 = self.m2 - d * (x - self.mu)
        if self.n >= 2:
            self.sd = (self.m2 / (self.n - 1 + 10 ** -32)) ** 0.5
        return x

    def numNorm(self, x):
        return (x is None and 0.5) or (x - self.lo) / (self.hi - self.lo + 10 ** -32)

    def numXpect(i, j):
        n = i.n + j.n + 0.00001
        return i.n / n * i.sd + j.n / n * j.sd
