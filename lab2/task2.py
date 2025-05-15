a = float(input("Введіть перше число: "))
b = float(input("Введіть друге число: "))
c = float(input("Введіть третє число: "))

total_sum = a + b + c
total_product = a * b * c

print("Сума введених чисел:", int(total_sum) if total_sum.is_integer() else total_sum)
print("Добуток введених чисел:", int(total_product) if total_product.is_integer() else total_product)
