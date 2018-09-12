import math


class Sym:
    def __init__(self):
        self.counts = []
        self.mode = None
        self.most = 0
        self.n = 0
        self._ent = None

    def symInc(self, x):
        if x is None:
            return x
        self._ent = None
        self.n = self.n + 1
        old = self.counts[x]
        new = old and old + 1 or 1
        self.counts[x] = new
        if new > self.most:
            self.most, self.mode = new, x
        return x

    def symDec(self, x):
        self._ent = None
        if self.n > 0:
            self.n = self.n - 1
            self.counts[x] = self.counts[x] - 1
        return x

    def symEnt(self):
        if not self._ent:
            self._ent = 0
            for x, n in enumerate(self.counts):
                p = n / self.n
                self._ent = self._ent - p * math.log(p, 2)
        return self._ent
