import random

words = ['boring', 'exhosting', 'tied']

word = random.choice(words)
letter = random.choice(word)

masked_word = word.replace(letter, '?', 1)

print("Вгадайте літеру у слові:", masked_word)

guess = input("Яка це літера? ")

if guess == letter:
    print("Правильно!")
else:
    print(f"Неправильно. Правильна літера: {letter}")
