text = "Хто б міг подумати, що в таких умовах може знайтися місце для ІТ"

words = text.split()

filtered_words = [word for word in words if not word.lower().startswith('м')]

result = ' '.join(filtered_words)

print(result)
