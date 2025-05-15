import random

numbers = [random.randint(0, 255) for _ in range(1000)]

average = sum(numbers) / len(numbers)

closest = min(numbers, key=lambda x: abs(x - average))

print("Середнє значення:", average)
print("Найближчий до середнього елемент:", closest)
