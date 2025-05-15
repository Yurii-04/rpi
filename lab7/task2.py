import random

numbers = [random.randint(-100, 100) for _ in range(1000)]

min_index = numbers.index(min(numbers))
max_index = numbers.index(max(numbers))

# діапазон між індексами
start = min(min_index, max_index) + 1
end = max(min_index, max_index)

positive_count = sum(1 for x in numbers[start:end] if x > 0)

print("Мінімальний елемент:", numbers[min_index], "на позиції", min_index)
print("Максимальний елемент:", numbers[max_index], "на позиції", max_index)
print("Кількість додатних елементів між ними:", positive_count)
