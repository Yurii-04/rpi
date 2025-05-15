# task 1
L = [3, 6, 7, 4, -5, 4, 3, -1]

total = sum(L)
if total > 2:
    print(len(L))

# task 2
min_elem = min(L)
max_elem = max(L)

diff = abs(max_elem - min_elem)

if diff > 10:
    print(sorted(L))
else:
    print("різниця менше 10")

# task 3-7
original = ['H', 'B']
final = original + ['T']
final = final * 5
del final[0]
print(final)


def f(x, y):
    return x + y


print(f(['2'], ['3', '4']))

if 7 in L:
    print(True)
