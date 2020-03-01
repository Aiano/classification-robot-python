from math import *

# all use cm
l1 = 10.5
l2 = 4.0
l3 = 11.5
l4 = 13.4
l5 = 12.0
s1 = 3.1
s2 = 11.5
s3 = 3.8
s4 = 1.8


def inverse_kinematic(x: float, y: float, z: float) -> (int, int, int, int):
    # we use degree measure on a1-4,
    # and use radian measure on others

    # Here are all values we will use
    global l1, l2, l3, l4, l5, s1, s2, s3, s4
    # a1: int
    # a2: int
    # a3: int
    # a4: int
    # b1: float
    # b2: float
    # b3: float
    # b4: float
    # b5: float
    # b6: float
    # b7: float
    # b8: float
    # b9: float
    # b10: float
    # b11: float
    # b12: float
    # d1: float
    # d2: float
    # d3: float
    # d4: float
    # d5: float
    # d6: float
    # d7: float
    # Above are all values we will use

    # Calculating
    d1 = sqrt(pow(x, 2) + pow(y, 2))
    d2 = d1 - l2
    d3 = sqrt(pow(l1, 2) + pow(d2, 2))
    d4 = z + l5

    b1 = acos(cosine_theorem(d2, d3, l1))
    b2 = pi / 2 - b1
    b3 = acos(cosine_theorem(l1, d3, d2))

    d5 = cosine_theorem_line(d3, b2, d4)
    d6 = sqrt(pow(s4, 2) + pow(l4, 2))

    b4 = acos(cosine_theorem(d3, d5, d4))
    b5 = acos(cosine_theorem(l3, d5, d6))
    b6 = acos(cosine_theorem(d5, d4, d3))
    b7 = acos(cosine_theorem(d5, d6, l3))
    b8 = acos(cosine_theorem(l3, d6, d5))
    b9 = atan(s4 / l4)
    b10 = pi - (b8 - b9)

    d7 = cosine_theorem_line(l3, b10, s1)

    b11 = acos(cosine_theorem(l3, d7, s1))
    b12 = acos(cosine_theorem(s3, d7, s2))

    a1 = radium_to_degree(pi / 2 * 3 - b3 - b4 - b5)
    a2 = radium_to_degree(b3 + b4 + b5 + b11 + b12 - pi)
    a3 = radium_to_degree(pi - (b7 + b6 - (pi / 2 - b9)))
    a4 = radium_to_degree(atan(x / y)) + 90

    return a1, a2, a3, a4


def cosine_theorem(left_side: float, right_side: float, opposite_side: float) -> float:
    # return the cosine value of an angle in a triangle using radium measure
    # cos theta = (a^2 + b^2 - c^2)/(2 * a * b)
    return (pow(left_side, 2) + pow(right_side, 2) - pow(opposite_side, 2)) / (2 * left_side * right_side)


def cosine_theorem_line(left_side: float, included_angle: float, right_side: float) -> float:
    # return the opposite side in a triangle
    # c = sqrt(a^2 + b^2 - 2 * a * b * cos theta)
    return sqrt(pow(left_side, 2) + pow(right_side, 2) - 2 * left_side * right_side * cos(included_angle))


def radium_to_degree(radium: float) -> int:
    return int(radium / pi * 180)
