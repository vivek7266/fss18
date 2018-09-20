from w3.num import Num
from w3.sym import Sym
import re
from helper.testutils import O


class Data:
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
            if not re.match('\?', x):
                c = len(self._use) + 1
                self._use[c] = c0
                self.name[c] = x
                if re.match(r'[<>%$]', x):
                    self.nums[c] = Num()
                else:
                    self.syms[c] = Sym()
                if re.match(r'<', x):
                    self.w[c] = -1
                elif re.match(r'>', x):
                    self.w[c] = 1
                elif re.match(r'!', x):
                    self.label_class = c
                else:
                    indeps.append(c)
        return

    def row(self, cells):
        r = len(self.rows)
        self.rows.append([])
        for c, c0 in enumerate(self._use):
            x = cells[c0]
            if x != "?":
                if self.nums[c]:
                    x = float(x)
                    self.nums.numInc(self.nums[c], x)
                else:
                    self.syms.symInc(self.nums[c], x)
            self.rows[r][c] = x
        return

    def rows1(self, file):
        with open(file) as fs:
            first = True
            for line in fs.readlines():
                line = re.sub(r'([\r\n\t ]|#.*)', '', line)
                line = re.sub(r'#.*', '', line)
                cells = line.split(',')
                if len(cells) > 0:
                    if first:
                        first = False
                        self.header(cells)
                    else:
                        self.row(cells)
        return self


@O.k
def testingData():
    data = Data()
    data = data.rows1("weather.csv")
    print(len(data.rows))
    for k, v in data.syms:
        print(data.name[k], v.n, v.mode, v.most)


if __name__ == "__main__":
    O.report()
