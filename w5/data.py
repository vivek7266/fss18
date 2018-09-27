from w3.num import Num
from w3.sym import Sym
import re
import sys
from helper.testutils import O
import w3.config as conf
import random
from functools import reduce


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
        return c not in self.w and self.label_class != c

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

    def dom(self, row1, row2):
        s1, s2, n = 0, 0, len(self.w)

        for c in self.w:
            a0 = row1[c]
            b0 = row2[c]
            a = self.nums[c].numNorm(a0)
            b = self.nums[c].numNorm(b0)
            s1 -= 10 ** (self.w[c] * (a - b) / n)
            s2 -= 10 ** (self.w[c] * (b - a) / n)
        return s1 / n < s2 / n

    def another(self, row1):
        row2 = random.randrange(len(self.rows))
        return self.rows[row2] if row1 != row2 else self.another(row1)

    def doms(self):
        n = conf.DOM['sample']
        # self.name.append('>dom') if '>dom' not in self.name else True
        res = []
        for r1 in range(len(self.rows)):
            row1 = self.rows[r1]
            row1.append(0)
            for s in range(n):
                row2 = self.another(r1)
                if self.dom(row1, row2):
                    row1[-1] += 1 / n
            res.append(self.rows[r1])
        return res


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
    data = rows("../w4/weatherLong.csv")
    print(','.join(data.name) + ",>dom")
    rows_with_doms = data.doms()
    for d in rows_with_doms:
        print("{0[0]},{0[1]},{0[2]},{0[3]},{0[4]},{0[5]:.2f}".format(d))
    """
    sort on humidity and check dom scores
    """
    sorted_humidity = sorted(rows_with_doms, key=lambda x: x[2])
    # print(sorted_humidity)
    for idx in range(len(sorted_humidity) - 1):
        """
        assert that if two adjacent items in  the sorted rows have difference in humidity then
        the next item with higher humidity should have a lower dom score.
        """
        # print(sorted_humidity[idx][5], " ---  ", sorted_humidity[idx + 1][5])
        assert sorted_humidity[idx][5] >= sorted_humidity[idx + 1][5] \
               or round(sorted_humidity[idx][5]) == round(sorted_humidity[idx + 1][5]) \
            if sorted_humidity[idx][2] < sorted_humidity[idx + 1][2] else True

    print("\n\n\n")
    data = rows("../w4/auto.csv")
    print(','.join(data.name) + ",>dom")
    rows_with_doms = data.doms()
    for d in rows_with_doms:
        print("{0[0]},{0[1]},{0[2]},{0[3]},{0[4]},{0[5]},{0[6]},{0[7]},{0[8]:.2f}".format(d))
    """
    sort together on (-1)weight, (1)acceltn, (1)mpg
    """
    sorted_auto_data = sorted(rows_with_doms, key=lambda x: (x[3], -x[4], -x[7]))
    # print(sorted_auto_data)
    """
    check if the average of bottom 10 dom scores is lower than top 10 
    """
    avg_dom_top = reduce(lambda x, y: float(x) + float(y), map(lambda x: x[-1], sorted_auto_data[:10])) / 10
    avg_dom_bottom = reduce(lambda x, y: float(x) + float(y), map(lambda x: x[-1], sorted_auto_data[-10:])) / 10
    # print(avg_dom_top, " -- ", avg_dom_bottom)
    assert avg_dom_top > avg_dom_bottom


if __name__ == "__main__":
    O.report()
