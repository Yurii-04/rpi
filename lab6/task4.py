import random

secret_number = random.randint(1, 100)

print("Я загадав число від 1 до 100. Спробуй вгадати!")
print("Введи 'вихід', щоб завершити гру.")

while True:
    guess = input("Введи своє число: ")

    if guess.lower() == 'вихід':
        print("Гру завершено. Загадане число було:", secret_number)
        break

    if not guess.isdigit():
        print("Будь ласка, введи число або 'вихід'.")
        continue

    guess = int(guess)

    if guess < secret_number:
        print("Загадане число більше.")
    elif guess > secret_number:
        print("Загадане число менше.")
    else:
        print("Вітаю! Ти вгадав число!")
        break
