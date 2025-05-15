L = [-8, 8, 6.0, 5, 'стрічка', -3.1]

total = 0

for elem in L:
    if type(elem) == int or type(elem) == float:
        total += elem

print("Сума чисел у списку:", total)
