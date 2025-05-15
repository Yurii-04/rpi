num_str = input("Введіть число: ")

total = 0
for ch in num_str:
    if ch.isdigit():
        digit = int(ch)
        if digit % 2 == 1:
            total += digit**2

print("Сума квадратів непарних цифр:", total)
