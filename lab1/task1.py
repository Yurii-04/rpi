def fahrenheit_to_celsius(tf):
    return 5/9 * (tf - 32)

def celsius_to_fahrenheit(tc):
    return 9/5 * tc + 32

tf = float(input("Введіть температуру у Фаренгейтах: "))
tc = fahrenheit_to_celsius(tf)
print(f"{tf}°F = {tc:.2f}°C")

tc = float(input("Введіть температуру у Цельсіях: "))
tf = celsius_to_fahrenheit(tc)
print(f"{tc}°C = {tf:.2f}°F")