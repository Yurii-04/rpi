import random

def play_level2():
    secret_number = random.randint(1, 100)

    while True:
        guess = int(input("Вгадайте число від 1 до 100: "))

        if guess == secret_number:
            print("Перемога!")
            break
        elif guess < secret_number:
            print("Більше")
        else:
            print("Менше")