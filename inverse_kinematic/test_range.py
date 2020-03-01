from inverse_kinematic.inverse_kinematic import *

for x in range(-10, 11, 1):
    for y in range(12, 27, 1):
        (a1, a2, a3, a4) = inverse_kinematic(x, y, 3)
        print("X:", x, "\tY:", y, "\tZ:", 0, "\ta1:", a1, "\ta2:", a2, "\ta3:", a3, "\ta4:", a4)
