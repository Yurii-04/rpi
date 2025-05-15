import requests

API_KEY = 'e88ff847f75e96b61790417313f59cf5'
CITY = 'Lviv'
URL = f'https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric'

response = requests.get(URL)
data = response.json()

if response.status_code == 200:
    temp_celsius = data['main']['temp']
    temp_fahrenheit = temp_celsius * 9 / 5 + 32

    print(f"Температура в {CITY}:")
    print(f"{temp_celsius:.1f}°C")
    print(f"{temp_fahrenheit:.1f}°F")

    if temp_celsius >= 20:
        print("Погода чудова! Варто прогулятись або зайнятись спортом на вулиці 🏃‍♂️")
    elif 10 <= temp_celsius < 20:
        print("Непогано для прогулянки, вдягнись тепліше 🙂")
    else:
        print("На вулиці холодно, краще займатись у приміщенні 🏠")
else:
    print("Помилка при отриманні даних про погоду.")
