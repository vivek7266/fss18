from w3.num import Num
from w3.sym import Sym
import re
import sys
from helper.testutils import O
import w3.config as conf
import random
import math


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
        if len(self.w) == 0: return
        n = conf.DOM['sample']
        self.name.append('>dom') if '>dom' not in self.name else True
        res = []
        for r1 in range(len(self.rows)):
            row1 = self.rows[r1]
            row1.append(0)
            for s in range(n):
                row2 = self.another(r1)
                if self.dom(row1, row2):
                    row1[-1] += 1 / n
            res.append(self.rows[r1])
        return self

    def unsuper(self):
        rows = self.rows
        enough = len(rows) ** conf.UNSUPER['enough']
        most = 0

        def band(c, lo, hi):
            if lo == 0:
                return "..{}".format(rows[hi][c])
            elif hi == most:
                return "{}..".format(str(rows[lo][c]))
            else:
                return "{}..{}".format(str(rows[lo][c]), str(rows[hi][c]))

        def argmin(c, lo, hi):
            cut = None
            if hi - lo > 2 * enough:
                l = Num()  # left split
                r = Num()  # right split

                # push everything in the right
                for i in range(lo, hi):
                    r.numInc(rows[i][c])

                best = r.sd  # currently all data is in right so best is sd on right
                # print(best)
                # push to the left one by one and keep track of best
                for i in range(lo, hi):
                    x = rows[i][c]
                    l.numInc(x)
                    r.numDec(x)
                    if l.n >= enough and r.n >= enough:
                        tmp = Num.numXpect(l, r) * 1.05
                        # print(tmp, x)
                        if tmp < best:
                            cut, best = i, tmp
                            # print(tmp, best)
            return cut

        def cuts(c, lo, hi, pre):
            txt = "{}{}..{}".format(pre, str(rows[lo][c]), str(rows[hi][c]))
            cut = argmin(c, lo, hi)
            # print(cut)
            if cut:
                print(txt)
                cuts(c, lo, cut, "{}|.. ".format(pre))
                cuts(c, cut + 1, hi, "{}|.. ".format(pre))
            else:
                b = band(c, lo, hi)
                print(txt + " (" + b + ")")
                for i in range(lo, hi + 1):
                    rows[i][c] = b

        def stop(c):
            # look for ? and return accordingly
            for i in range(len(rows) - 1, 0, -1):
                if rows[i][c] != "?":
                    return i
            return 0

        for c in self.indeps:
            if c in self.nums:
                # sort all the rows and push ? at the bottom
                rows = sorted(rows, key=lambda x: 10 ** 32 if x[c] == '?' else x[c])
                # print(["{}:{}".format(i, row) for i, row in enumerate(rows)])
                # find the max num of rows to worry about
                most = stop(c)
                print('\n--' + str(self.name[c] + ', most = ' + str(most) + '------------------'))
                cuts(c, 0, most, '|.. ')
        print(", ".join(self.name))
        for i in rows:
            print("\t".join(str(r) for r in i))
        return rows

    def super(self):
        rows = self.rows
        enough = len(rows) ** conf.UNSUPER['enough']
        goal = len(self.name) - 1
        most = 0

        def band(c, lo, hi):
            if lo == 0:
                return "..{}".format(rows[hi][c])
            elif hi == most:
                return "{}..".format(str(rows[lo][c]))
            else:
                return "{}..{}".format(str(rows[lo][c]), str(rows[hi][c]))

        def argmin(c, lo, hi):
            cut = None
            xl, yl = Num(), Num()  # left split for both features and label cols
            xr, yr = Num(), Num()  # right split for both features and label cols

            # push everything in the right
            for i in range(lo, hi):
                xr.numInc(rows[i][c])
                yr.numInc(rows[i][goal])

            best_x = xr.sd  # currently all data is in right so best is sd on right
            best_y = yr.sd  # currently all data is in right so best is sd on right
            mu = yr.mu
            # print(best)
            # push to the left one by one and keep track of best
            if hi - lo > 2 * enough:
                for i in range(lo, hi):
                    x = rows[i][c]
                    y = rows[i][goal]
                    xl.numInc(x)
                    yl.numInc(y)
                    xr.numDec(x)
                    yr.numDec(y)
                    if xl.n >= enough and xr.n >= enough:
                        tmp_x = xl.numXpect(xr) * 1.05
                        tmp_y = yl.numXpect(yr) * 1.05
                        # print(tmp, x)
                        try:
                            if tmp_x < best_x:
                                if tmp_y < best_y:
                                    cut, best_x, best_y = i, tmp_x, tmp_y
                                    # print(tmp_x, tmp_y, best_x, best_y)
                        except:
                            print(tmp_x, tmp_y)
            return cut, mu

        def cuts(c, lo, hi, pre):
            txt = "{}{}..{}".format(pre, str(rows[lo][c]), str(rows[hi][c]))
            cut, mu = argmin(c, lo, hi)
            # print(cut)
            if cut:
                print(txt)
                cuts(c, lo, cut, "{}|.. ".format(pre))
                cuts(c, cut + 1, hi, "{}|.. ".format(pre))
            else:
                b = band(c, lo, hi)
                print("{} ==> {}".format(txt, math.floor(100 * mu)))
                for i in range(lo, hi + 1):
                    rows[i][c] = b

        def stop(c):
            # look for ? and return accordingly
            for i in range(len(rows) - 1, 0, -1):
                if rows[i][c] != "?":
                    return i
            return 0

        for c in self.indeps:
            if c in self.nums:
                # sort all the rows and push ? at the bottom
                rows = sorted(rows, key=lambda x: 10 ** 32 if x[c] == '?' else x[c])
                # print(["{}:{}".format(i, row) for i, row in enumerate(rows)])
                # find the max num of rows to worry about
                most = stop(c)
                print('\n--' + str(self.name[c] + ', most = ' + str(most) + '------------------'))
                cuts(c, 0, most, '|.. ')
        print(", ".join(self.name))
        for i in rows:
            print("\t".join(str(r) for r in i))
        return rows


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
def testSuper():
    data = rows("../w4/auto.csv")
    data = data.doms()
    disc_rows = data.super()
    # print(disc_rows)

    data_1 = rows("../w4/weatherLong.csv")
    data_1 = data_1.doms()
    disc_rows_1 = data_1.super()
    # print(disc_rows)
    assert disc_rows_1[0][1] == '..69.0'



if __name__ == "__main__":
    O.report()
