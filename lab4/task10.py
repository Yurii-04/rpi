import random

gamer1_roll = random.randint(1, 6)
gamer2_roll = random.randint(1, 6)

print(f"Гравець 1 кинув: {gamer1_roll}")
print(f"Гравець 2 кинув: {gamer2_roll}")

if gamer1_roll > gamer2_roll:
    print("Переміг Гравець 1!")
elif gamer2_roll > gamer1_roll:
    print("Переміг Гравець 2!")
else:
    print("Нічия!")
