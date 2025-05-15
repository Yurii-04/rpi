def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

numbers = [3, 4, 7, 10, 13, 17, 20, 23, 30]

prime_sum = sum(num for num in numbers if is_prime(num))

print("Сума простих чисел:", prime_sum)
