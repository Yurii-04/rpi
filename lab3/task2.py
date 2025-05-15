def max_of_two(a, b):
    return a if a > b else b

num1 = float(input("Введіть перше число: "))
num2 = float(input("Введіть друге число: "))

print(f"Максимальне число: {max_of_two(num1, num2)}")
