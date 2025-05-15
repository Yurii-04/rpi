text = input("Введіть довільний текст: ")

digits = [int(ch) for ch in text if ch.isdigit()]

if digits:
    print("Цифри у тексті:", digits)
    print("Кількість цифр:", len(digits))
    print("Сума цифр:", sum(digits))
    print("Максимальна цифра:", max(digits))
else:
    print("У тексті немає цифр.")
