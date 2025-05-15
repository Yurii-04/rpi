try:
    money = float(input("Скільки у вас є грошей (в USD)? "))
    coffee_price = 5
    croissant_price = 3
    total_price = coffee_price + croissant_price

    if money >= total_price:
        print("Ви можете купити каву з круасаном!")
    elif money >= coffee_price:
        print("Ви можете дозволити собі тільки каву.")
    else:
        print("На жаль, недостатньо грошей навіть на каву.")
except ValueError:
    print("Будь ласка, введіть коректне числове значення.")
