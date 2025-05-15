import random

numbers = [random.randint(0, 255) for _ in range(20)]

max_sum = None
max_start_index = 0

for i in range(len(numbers) - 5 + 1):
    current_sum = sum(numbers[i:i+5])
    if max_sum is None or current_sum > max_sum:
        max_sum = current_sum
        max_start_index = i

max_sublist = numbers[max_start_index:max_start_index+5]

print("Список чисел:", numbers)
print("Максимальна сума 5 сусідніх елементів:", max_sum)
print("Ці 5 елементів:", max_sublist)
