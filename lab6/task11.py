import random

N = 4
M = 5
matrix = [[random.randint(0, 5) for _ in range(M)] for _ in range(N)]

for row in matrix:
    print(row)

max_same_count = 0
max_row_index = -1

for i, row in enumerate(matrix):
    counts = {}
    for num in row:
        counts[num] = counts.get(num, 0) + 1
    same_count = max(counts.values())
    if same_count > max_same_count:
        max_same_count = same_count
        max_row_index = i

print(f"\nНомер рядка з максимальною кількістю однакових елементів: {max_row_index}")
print(f"Цей рядок: {matrix[max_row_index]}")
