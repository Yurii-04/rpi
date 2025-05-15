import random

numbers = [random.randint(0, 255) for _ in range(1000)]

found = False
for i in range(len(numbers) - 1):
    if numbers[i] % 2 == 1 and numbers[i+1] % 2 == 1:
        print(f"Пара сусідніх непарних чисел: {numbers[i]}, {numbers[i+1]}")
        found = True

if not found:
    print("Сусідніх непарних чисел немає")
