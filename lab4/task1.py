from triangle_calculator import triangle_area

a = float(input("Введіть довжину сторони a: "))
b = float(input("Введіть довжину сторони b: "))
c = float(input("Введіть довжину сторони c: "))

result = triangle_area(a, b, c)
print(f"Площа трикутника: {result:.2f}")