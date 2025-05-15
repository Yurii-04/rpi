def calculate_bmi(weight_kg, height_m):
    return weight_kg / (height_m ** 2)

def interpret_bmi(bmi):
    if bmi < 18.5:
        return "Недостатня вага"
    elif 18.5 <= bmi < 25:
        return "Нормальна вага"
    elif 25 <= bmi < 30:
        return "Надмірна вага"
    else:
        return "Ожиріння"

weight = 62  # кг
height = 1.70  # м

bmi = calculate_bmi(weight, height)
category = interpret_bmi(bmi)

print(f"Ваш ІМТ: {bmi:.2f}")
print(f"Категорія: {category}")
