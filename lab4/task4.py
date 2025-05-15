from guess_game_lvl1 import play_level1
from guess_game_lvl2 import play_level2

print("Виберіть рівень складності:")
print("1 - Одна спроба")
print("2 - З підказками")
level = int(input("Введіть 1 або 2: "))

if level == 1:
    play_level1()
elif level == 2:
    play_level2()
else:
    print("Невірний вибір рівня!")