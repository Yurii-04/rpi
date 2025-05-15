import random


def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True


numbers = [random.randint(0, 255) for _ in range(1000)]
prime_sum = sum(num for num in numbers if is_prime(num))
print("Сума простих чисел у списку:", prime_sum)
