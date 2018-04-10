from Math24DP import solveDP
from time import time

tasks = [(6, 6, 6, 6), (1, 2, 3, 4, 5), (1, 2, 3, 4, 5, 6)]

for task in tasks:
    start = time()
    print(len(solveDP(*task)))
    print(time() - start)
    print()

print(solveDP(6, 6, 6, 6))