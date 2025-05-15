import random

numbers = [random.randint(0, 255) for _ in range(1000)]

count = 0
length = 1

for i in range(1, len(numbers)):
    if numbers[i] > numbers[i-1]:
        length += 1
    else:
        if length >= 4:
            count += 1
        length = 1

# Перевірка останнього проміжку
if length >= 4:
    count += 1

print("Кількість проміжків монотонного зростання (4 і більше):", count)
