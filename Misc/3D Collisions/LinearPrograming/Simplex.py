import imp
imp.load_source('Tableau', 'C:/Users/lukeh_000/Documents/Programs/Python/LinearPrograming/Tableau.py')
from Tableau import Tableau
def phase1(T):
    # If Tableau is already feasible exit.
    feasible = True
    for i in range(T.h):
        if T.get(i, "1 ") < 0:
            feasible = False
    if feasible:
        return True
    # Add x0 column and z0 row.
    T.addrow(T.h, [0 for j in range(T.w)], "z0")
    col = []
    for i in range(T.h):
        label = T.iLabels[i]
        if label[0] == "x":
            col += [T.get(i, "1 ") < 0]
        elif label == "z0":
            col += [1]
        else:
            col += [0]
    T.addcol(T.w-1, col, "x0")
    # Pivot on minimum element to make feasible.
    mindex = 0
    minimum = 0
    for i in T.anticyclecol(): # Uses anticycle just to get the rows to check
        value = T.get(i, "1 ")
        if value < minimum:
            minimum = value
            mindex = i
    T.pivot(mindex, "x0")
    # Now minimize z0, but always pivot on x0 if possible.
    while True:
        # Try to pivot on x0
        for j in T.anticyclerow():
            if T.get("z0", j) > 0:
                continue
            value = T.get("x0", j)
            if value >= 0:
                continue
            minRatio = -T.get("x0", "1 ")/value
            miner = False
            for i in T.anticyclecol():
                value = T.get(i, j)
                endValue = T.get(i, "1 ")
                if value < 0 and -endValue/value < minRatio:
                    miner = True
                    break
            if miner is False: # If this is true, then after the pivot T will be feasible w/ x0 = 0
                T.pivot("x0", j)
                T.removecol("x0")
                T.removerow("z0")
                return True
        # Otherwise use anti-cycling rule
        progress = False
        minRatio = 0 # Gets manually assigned
        for s in T.anticyclerow():
            if T.get("z0", s) >= 0:
                continue
            r = 0
            for i in T.anticyclecol():
                value = T.get(i, s)
                endValue = T.get(i, "1 ")
                if value >= 0:
                    continue
                ratio = -endValue/value
                if not progress:
                    progress = True
                    minRatio = ratio #Here
                    r = i
                elif ratio < minRatio:
                    minRatio = ratio
                    r = i
            if not progress:
                continue
            T.pivot(r, s)
            break
        if progress is False:
            T.removerow("x0")
            T.removerow("z0")
            return False

def phase2(T):
    dualMethod(T)
    if not phase1(T):
        return False
    while True:
        progress = False
        for s in T.anticyclerow():
            if T.get("z ", s) >= 0:
                continue
            for i in T.anticyclecol():
                value = T.get(i, s)
                if value >= 0:
                    continue
                ratio = -T.get(i, "1 ")/value
                if not progress:
                    progress = True
                    minRatio = ratio
                    r = i
                elif ratio < minRatio:
                    minRatio = ratio
                    r = i
            if not progress:
                continue
            T.pivot(r, s)
            break
        if progress is False:
            return True

# This takes advantage of the dual nature of linear programs.
# This is included because it speeds up R3Region.getHamiltonian() <- In theory at least...
# Since I can pick an objective function which is all feasible for the dual LP

def dualMethod(T):
    if "z " in T.iLabels:
        for j in range(T.w):
            if T.get("z ", j) < 0:
                return False
    else:
        return False
    
    while True:
        progress = False
        for r in T.anticyclecol():
            if T.get(r, "1 ") >= 0:
                continue
            for j in T.anticyclerow():
                value = T.get(r, j)
                if value <= 0:
                    continue
                ratio = T.get("z ", j)/value
                if not progress:
                    progress = True
                    minRatio = ratio
                    s = j
                elif ratio < minRatio:
                    minRatio = ratio
                    s = j
            if not progress:
                continue
            T.pivot(r, s)
            break
        if progress is False:
            return True
