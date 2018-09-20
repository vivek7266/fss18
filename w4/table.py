from w3.num import Num
from w3.sym import Sym
import re


class Table:
    def __init__(self):
        self.w = []
        self.syms = []
        self.nums = []
        self.label_class = None
        self.rows = []
        self.name = []
        self._use = []

    def indep(self, c):
        return not (self.w[c] and self.label_class != c)

    def dep(self, c):
        return not self.indep(c)

    def header(self, cells):
        indeps = []
        for c0, x in enumerate(cells):
            if not re.match('%?', x):
                c = len(self._use) + 1
                self._use[c] = c0
                self.name[c] = x
                if re.match("[<>%$]", x):
                    self.nums[c] = Num()
                else:
                    self.syms[c] = Sym()
                if re.match("<", x):
                    self.w[c] = -1
                elif re.match(">", x):
                    self.w[c] = 1
                elif re.match("!", x):
                    self.label_class = c
                else:
                    indeps.append(c)
        return


    def row(self, cells):
        r = len(self.rows) + 1
        self.rows[r] = []
        for c, c0 in enumerate(self._use):
            x = cells[c0]
            if x != "?":
                if self.nums[c]:
                    x = int(x)
                    Num.numInc(self.nums[c], x)
                else:
                    Num.numInc(self.nums[c], x)
            self.rows[r][c] = x
        return


    def rows(self, stream, file, f0, f):
        with open(file) as fs:
            for line in fs:
                yield line