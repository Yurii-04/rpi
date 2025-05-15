import math


def calculate_function(x):
    if 0.2 <= x <= 0.9:
        return math.sin(x)
    else:
        return 1


try:
    x = float(input("Введіть дійсне число x: "))
    result = calculate_function(x)
    print(f"Значення функції f({x}) = {result}")
except ValueError:
    print("Помилка! Введіть коректне дійсне число.")