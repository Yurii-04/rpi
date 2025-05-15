from calculate_expression import calculate_expression

x = float(input("Введіть значення x (у радіанах): "))
result = calculate_expression(x)
print(f"Значення виразу √(1 - sin²x) для x = {x}: {result:.4f}")