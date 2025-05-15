import datetime

try:
    temp = float(input("Яка зараз температура повітря (в °C)? "))
    rain_input = input("Чи йде дощ? (так/ні): ").strip().lower()

    is_raining = rain_input in ["так", "т", "yes", "y"]

    now = datetime.datetime.now()
    current_day = now.strftime("%a")
    current_hour = now.hour

    good_weather = 10 <= temp <= 25 and not is_raining
    is_gym_day = current_day in ["Mon", "Wed", "Fri"] and current_hour >= 16

    if good_weather or is_gym_day:
        print("Час піти на пробіжку або прогулянку!")
    else:
        print("Сьогодні краще залишитись вдома або піти до тренажерного залу.")
except ValueError:
    print("Введіть правильні числові дані для температури.")
