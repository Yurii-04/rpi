import random

numbers = [random.randint(0, 255) for _ in range(1000)]

count = sum(1 for num in numbers if num > 100)

print("Кількість чисел більших за 100:", count)
