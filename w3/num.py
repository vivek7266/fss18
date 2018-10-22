from w3.sample import Sample
from helper.testutils import O
import w3.config as conf


class Num:
    def __init__(self, max=1000):
        self.n = 0
        self.mu = 0
        self.m2 = 0
        self.sd = 0
        self.lo = conf.MAGIC_PARAMS['lo']
        self.hi = conf.MAGIC_PARAMS['hi']
        self.some = Sample(max)
        self.w = 1

    def numInc(self, x):
        if x is None or x == "?":
            return x
        self.n = self.n + 1
        self.some.sampleInc(x)
        d = x - self.mu
        self.mu = self.mu + (d / self.n)
        self.m2 = self.m2 + (d * (x - self.mu))
        if x > self.hi:
            self.hi = x
        if x < self.lo:
            self.lo = x
        if self.n >= 2:
            self.sd = (self.m2 / (self.n - 1 + 10 ** -32)) ** 0.5
        return x

    def numDec(self, x):
        if x is None or x == "?" or self.n == 1:
            return x
        self.n = self.n - 1
        d = x - self.mu
        self.mu = self.mu - (d / self.n)
        var = self.m2 - (d * (x - self.mu))
        if var < 0:
            var = 0
        self.m2 = var
        if self.n >= 2:
            self.sd = (self.m2 / (self.n - 1 + 10 ** -32)) ** 0.5
        return x

    # def numNorm(self, x):
    #     return ((x is None or x == "?") and 0.5) or (x - self.lo) / (self.hi - self.lo + conf.MAGIC_PARAMS['tiny'])

    def numNorm(self, x):
        return (x - self.lo) / (self.hi - self.lo + (10 ** -32))

    def numXpect(i, j):
        n = i.n + j.n + 0.00001
        return i.n / n * i.sd + j.n / n * j.sd

    def nums(self, t, func=lambda x: x):
        n = Num()
        for x in t:
            self.numInc(func(x))
        return n


# @O.k
def testingNum():
    n = Num().nums([4, 10, 15, 38, 54, 57, 62, 83, 100, 100, 174, 190, 215, 225,
                    233, 250, 260, 270, 299, 300, 306, 333, 350, 375, 443, 475,
                    525, 583, 780, 1000])

    print(n.mu)
    print(round(n.sd, 3))
    assert n.mu == 270.3 and round(n.sd, 3) == 231.946

# if __name__ == "__main__":
#     O.report()
