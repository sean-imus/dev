inputStr = float("17.5")

import math

sidelength = float(inputStr)

area = sidelength * sidelength

hunger_per_person = 100

fed_people = math.floor(area / hunger_per_person)

print(fed_people)

