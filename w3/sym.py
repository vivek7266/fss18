import math
from helper.testutils import O


class Sym:
    def __init__(self):
        self.counts = {}
        self.mode = None
        self.most = 0
        self.n = 0
        self._ent = None

    def symInc(self, x):
        if x is None:
            return x
        self._ent = None
        self.n = self.n + 1
        old = self.counts.get(x, 0)
        new = old and old + 1 or 1
        self.counts[x] = new
        if new > self.most:
            self.most, self.mode = new, x
        return x

    def symDec(self, x):
        self._ent = None
        if self.n > 0:
            self.n = self.n - 1
            self.counts[x] = self.counts.get(x, 0) - 1
        return x

    def symEnt(self):
        if not self._ent:
            self._ent = 0
            for x, n in self.counts.items():
                p = n / self.n
                self._ent = self._ent - p * math.log(p, 2)
        return self._ent

    def syms(self, t, func=lambda x: x):
        s = Sym()
        [s.symInc(func(x)) for x in t]
        return s


# @O.k
def testingSym():
    s = Sym().syms(['y', 'y', 'n'])
    # print(s.symEnt())
    assert abs(s.symEnt() - 1) <= 0.5

    s = s.syms(['y', 'y', 'y', 'y', 'y', 'y', 'y', 'y', 'y', 'n', 'n', 'n', 'n', 'n'])
    print(s.counts)
    assert (round(s.symEnt(), 4) == 0.9403)


# if __name__ == "__main__":
#     O.report()
