total = 0

print("Вводьте числа по одному. Для завершення введіть 'стоп' або порожній рядок.")

while True:
    s = input("Введіть число: ").strip()

    if s.lower() == 'стоп' or s == '':
        break

    if s.replace('.', '', 1).isdigit() or (s.startswith('-') and s[1:].replace('.', '', 1).isdigit()):
        # Перетворюємо на float, щоб врахувати дійсні числа
        total += float(s)
    else:
        print("Будь ласка, введіть коректне число або 'стоп' для завершення.")

print("Сума введених чисел:", total)
