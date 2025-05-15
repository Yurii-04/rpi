coffee_price = 2.5
pizza_price = 5.0

coffee_count = int(input("Введіть кількість чашок кави: "))
pizza_count = int(input("Введіть кількість кусочків піци: "))

total = coffee_count * coffee_price + pizza_count * pizza_price

print(f"Загальна вартість замовлення: {total:.2f} USD")
