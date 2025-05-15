import random

def max_min_difference(numbers):
    return max(numbers) - min(numbers)

random_list = [random.randint(-20, 50) for _ in range(10)]

print("Список:", random_list)
print("Різниця між max і min:", max_min_difference(random_list))
