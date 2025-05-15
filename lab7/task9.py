import random

numbers = [random.randint(0, 255) for _ in range(1000)]

average = sum(numbers) / len(numbers)

count_above_average = sum(1 for num in numbers if num > average)

percentage = (count_above_average / len(numbers)) * 100

print(f"Середнє арифметичне: {average:.2f}")
print(f"Відсоток елементів, що перевищують середнє: {percentage:.2f}%")
