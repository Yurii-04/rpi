L = [1, 2, 3, 4, 5, 6, 7, 8]
N = len(L)

half = N // 2

if N % 2 == 0:
    new_L = L[half:] + L[:half]
else:
    new_L = L[half+1:] + [L[half]] + L[:half]

print("Новий список:", new_L)
