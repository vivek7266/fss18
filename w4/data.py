from w3.num import Num
from w3.sym import Sym
import re
import sys
from helper.testutils import O


class Data:
    def __init__(self):
        self.w = {}
        self.syms = {}
        self.nums = {}
        self.label_class = None
        self.rows = []
        self.name = []
        self._use = []
        self.indeps = []

    def indep(self, c):
        return not (self.w[c] and self.label_class != c)

    def dep(self, c):
        return not self.indep(c)

    def header(self, cells):
        indeps = []
        for c0, x in enumerate(cells):
            if not re.match('\?', x):
                c = len(self._use)
                self._use.append(c0)
                self.name.append(x)
                if re.match(r'[<>\$]', x):
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
                    self.indeps.append(c)
        return

    def row(self, cells):
        r = len(self.rows)
        self.rows.append([])
        for c, c0 in enumerate(self._use):
            x = cells[c0]
            if x != "?":
                if c in self.nums:
                    x = float(x)
                    self.nums[c].numInc(x)
                else:
                    self.syms[c].symInc(x)
            self.rows[r].append(x)
        return self

    def rows1(self, src):
        first = True
        for line in src:
            line = re.sub(r'([ \n\r\t]|#.*)', '', line)
            # line = re.sub(r'#.*', '', line)
            cells = line.split(',')
            if len(cells) > 0:
                if first:
                    first = False
                    self.header(cells)
                else:
                    self.row(cells)
        return self


def lines(src=None):
    if src is None:
        for line in sys.stdin:
            yield line
    elif src[-3:] in ["csv", ".dat"]:
        with open(src) as fs:
            for line in fs:
                yield line
    else:
        for line in src.splitlines():
            yield line


def rows(src):
    data = Data()
    return data.rows1(lines(src))


def print_data_stats(data):
    print("\n\n")
    print("\t\t\tn\tmode\tfrequency")
    for k, v in data.syms.items():
        print("{}\t{}\t{}\t{}\t{}".format(k + 1, data.name[k], v.n, v.mode, v.most))
    print("\n\t\tn\tmu\tsd")
    for k, v in data.nums.items():
        print('{0}\t{1}\t{2}\t{3:.2f}\t{4:.2f}'.format(k + 1, data.name[k], v.n, v.mu, v.sd))


@O.k
def testingData():
    # data = Data()
    # data = data.rows1("weather.csv")
    data = rows("weather.csv")
    print_data_stats(data)
    for k, v in data.syms.items():
        if data.name[k] == 'outlook':
            assert v.mode == 'sunny'
            assert v.most == 5
    for k, v in data.nums.items():
        if data.name[k] == '$temp':
            assert round(v.mu) == round(73.57)

    data = rows("weatherLong.csv")
    print_data_stats(data)
    for k, v in data.syms.items():
        if data.name[k] == 'outlook':
            assert v.mode == 'sunny'
            assert v.most == 10
    for k, v in data.nums.items():
        if data.name[k] == '<humid':
            assert round(v.mu) == round(81.64)

    data = rows("auto.csv")
    print_data_stats(data)
    for k, v in data.syms.items():
        if data.name[k] == 'origin':
            assert v.mode == '1'
            assert v.most == 249
    for k, v in data.nums.items():
        if data.name[k] == '>acceltn':
            assert round(v.mu) == round(15.57)


if __name__ == "__main__":
    O.report()
