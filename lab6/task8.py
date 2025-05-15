text = input("Введіть текст: ")

words = text.split()

max_len = 0
max_index = -1

for i, word in enumerate(words):
    if len(word) > max_len:
        max_len = len(word)
        max_index = i

print("Номер найдовшого слова:", max_index + 1)
print("Саме слово:", words[max_index])
