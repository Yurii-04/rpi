with open('planets.txt', 'r') as file:
    planets = file.readlines()

planets = [planet.strip() for planet in planets]
planets.sort()

with open('sort_planets.txt', 'w') as file:
    for planet in planets:
        file.write(planet + '\n')
