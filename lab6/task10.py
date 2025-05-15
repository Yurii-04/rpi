import random

N = 4
M = 5

matrix = [[random.randint(-10, 10) for _ in range(M)] for _ in range(N)]

for row in matrix:
    print(row)
