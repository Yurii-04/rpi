import random

def play_level1():
    secret_number = random.randint(1, 100)

    guess = int(input("Вгадайте число від 1 до 100 (у вас 1 спроба): "))

    if guess == secret_number:
        print("Перемога!")
    else:
        print("Спробуйте ще раз.")