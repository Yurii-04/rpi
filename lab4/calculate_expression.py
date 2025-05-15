import math


def calculate_expression(x):
    sin_squared = math.sin(x) ** 2

    # Перевірка, щоб уникнути комплексних чисел (1 - sin^2x >= 0)
    if 1 - sin_squared < 0:
        return "Вираз не визначений для цього значення (додатне значення під коренем)"

    result = math.sqrt(1 - sin_squared)
    return result


