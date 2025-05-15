import math


def calculate_expressions(x, y):
    """
    >>> calculate_expressions(0, 0)
    (0.0, 0.0)
    >>> calculate_expressions(1, 1)
    (1.0, 2.6375823365643407)
    >>> calculate_expressions(-1, -1)
    (1.0, -2.6375823365643407)
    """
    # Обчислення z
    numerator = x + (2 + y) / (x ** 2)
    denominator = 1 + y + 1 / math.sqrt(x ** 2 + 10)
    z = numerator / denominator

    # Обчислення q
    q = 2.8 * math.sin(x) + abs(y)

    return z, q


if __name__ == "__main__":
    import doctest

    doctest.testmod()