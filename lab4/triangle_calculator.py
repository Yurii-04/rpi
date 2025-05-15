import math

def triangle_area(a, b, c):
    # Перевірка умови існування трикутника (сума будь-яких двох сторін > третьої)
    if (a + b <= c) or (b + c <= a) or (a + c <= b):
        return "Трикутник із заданими сторонами не існує"

    p = (a + b + c) / 2

    area = math.sqrt(p * (p - a) * (p - b) * (p - c))
    return area