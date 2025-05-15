def is_even(number):
    return number % 2 == 0

num = int(input("Введіть число для перевірки: "))

if is_even(num):
    print(f"Число {num} парне.")
else:
    print(f"Число {num} непарне.")
