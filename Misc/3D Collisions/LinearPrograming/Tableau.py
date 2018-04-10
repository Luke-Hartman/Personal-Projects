import math
# Potential Bug, see getVertices. Hasn't come up yet.
class Tableau(object):
    
    def __init__(self, A, b, p, z=0):
        self.h, self.w = len(A) + 1, len(A[0]) + 1
        self.iLabels = ["x" + str(i + self.w) for i in range(self.h - 1)] + ["z "]
        self.jLabels = ["x" + str(j + 1) for j in range(self.w - 1)] + ["1 "]
        self.m = [[0 for a in range(self.w)] for a in range(self.h)]
        for i in range(self.h - 1):
            for j in range(self.w - 1):
                self.m[i][j] = float(A[i][j])
        for i in range(self.h - 1):
            self.m[i][-1] = -float(b[i])
        for j in range(self.w - 1):
            self.m[-1][j] = float(p[j])
        self.m[-1][-1] = z

    def __str__(self):
        m, h, w = self.m, self.h, self.w
        s = "\n            "
        for j in range(w):
            s += self.jLabels[j] + "       "
        s += "\n      "
        for j in range(w):
            s += "----------"
        s += "\n"
        for i in range(h):
            s += self.iLabels[i] + " = |"
            for j in range(w):
                value = m[i][j]
                length = 5
                if value != 0:
                    length -= int(math.log(math.fabs(value), 10))
                if value < 0:
                    length -= 1
                s += " " + "{0:.2f}".format(value)
            s += "\n"
        return s

    def pivot(self, r, s):
        r = self.index(r)
        s = self.index(s)
        m, h, w = self.m, self.h, self.w
        temp = self.iLabels[r]
        self.iLabels[r] = self.jLabels[s]
        self.jLabels[s] = temp
        Ars = m[r][s]
        new = [[0 for j in range(w)] for i in range(h)]
        new[r][s] = 1 / Ars
        for i in range(h):
            if i != r:
                new[i][s] = m[i][s] / Ars
        for j in range(w):
            if j != s:
                new[r][j] = -m[r][j] / Ars
        for i in range(h):
            for j in range(w):
                if i != r and j != s:
                    new[i][j] = m[i][j] - m[i][s] * m[r][j] / Ars
        self.m = new

    def get(self, i, j):
        i = self.index(i)
        j = self.index(j)
        return self.m[i][j]

    def getPostPivot(self, r, s, i, j):
        g = self.get
        return g(i, j) - g(i, s) * g(r, j) / g(r, s)

    # Gets all indices for pivots and the corresponding z values.
    def getVertices(self): #TODO POTENTIAL BUG, Ties for ratio test...
        vertices = []
        for s in self.anticyclerow():
            # Finds any possible pivots in col j
            first = True
            r = 0
            for i in self.anticyclecol():
                value = self.get(i, s)
                endValue =  self.get(i, "1 ")
                if value >= 0:
                    continue
                ratio = -endValue/value
                if first:
                    first = False
                    minRatio = ratio
                    r = i
                elif ratio < minRatio:
                    minRatio = ratio
                    r = i
            if first:
                continue
            # Now calculate z value.
            z = self.getPostPivot(r, s, self.index("z "), self.index("1 "))
            zeros = self.anticyclerow()
            for j in range(len(zeros)):
                if zeros[j] == s:
                    zeros[j] = r
            vertices += [[sorted(zeros), (r, s), z]]
        return vertices

    def addrow(self, i, row, label):
        self.m.insert(i, row)
        self.iLabels.insert(i, label)
        self.h += 1

    def addcol(self, j, col, label):
        for i in range(self.h):
            self.m[i].insert(j, col[i])
        self.jLabels.insert(j, label)
        self.w += 1

    def removerow(self, i):
        i = self.index(i)
        del self.m[i]
        del self.iLabels[i]
        self.h -= 1
        
    def removecol(self, j):
        j = self.index(j)
        for i in range(self.h):
            del self.m[i][j]
        del self.jLabels[j]
        self.w -= 1

    def permrows(self, perm):
        m = self.m
        new = []
        newLabels = []
        for i in perm:
            new.append(m[i])
            newLabels.append(self.iLabels[i])
        self.m = new
        self.iLabels = newLabels

    def permcols(self, perm):
        m = self.m
        new = []
        newLabels = []
        for i in range(self.h):
            row = []
            for j in perm:
                row.append(m[i][j])
            new.append(row)
        for j in perm:
            newLabels.append(self.jLabels[j])
        self.m = new
        self.jLabels = newLabels
        
    def index(self, label):
        if type(label) != str:
            return label
        for i in range(self.h):
            if label == self.iLabels[i]:
                return i
        for j in range(self.w):
            if label == self.jLabels[j]:
                return j
        return -1

    def getValue(self, label):
        for i in range(self.h):
            if label == self.iLabels[i]:
                return self.get(i, "1 ")
        for j in range(self.w):
            if label == self.jLabels[j]:
                return 0

    # Returns a sorted list of indices corresponding to the row labels
    def anticyclecol(self):
        return [label for label in sorted(self.iLabels) if label[0] == 'x']
    # Returns a sorted list of indices corresponding to the col labels
    def anticyclerow(self):
        return [label for label in sorted(self.jLabels) if label[0] == 'x']
        
        
