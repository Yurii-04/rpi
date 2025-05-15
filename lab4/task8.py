import math

def calculate_z(x, y):
    if x == 0:
        raise ValueError("x не може бути рівним нулю (ділення на x²)")

    numerator = x + (2 + y) / (x ** 2)
    denominator = y + 1 / math.sqrt(x ** 2 + 10)

    if denominator == 0:
        raise ValueError("Знаменник виразу дорівнює нулю")

    return numerator / denominator


def calculate_q(x, y):
    return 2.8 * math.sin(x) + abs(y)


if __name__ == "__main__":
    x = float(input("Введіть значення x: "))
    y = float(input("Введіть значення y: "))

    try:
        z_result = calculate_z(x, y)
        q_result = calculate_q(x, y)

        print(f"z = {z_result}")
        print(f"q = {q_result}")
    except ValueError as e:
        print(f"Помилка: {e}")