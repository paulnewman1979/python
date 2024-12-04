from Point import Point
from Ray import Ray
from Line import Line

def pp_to_line(p1, p2):
    a = p2.y - p1.y
    b = p1.x - p2.x
    c = - a * p1.x - b * p1.y

    return Line(a, b, c)

def pp_to_p_inner(p1, p2, r1, r2, name):
    x = (p1.x * r1 + p2.x * r2) / (r1 + r2)
    y = (p1.y * r1 + p2.y * r2) / (r1 + r2)

    return Point(x, y, name)

def pp_to_p_outer(p1, p2, r1, r2, name):
    x = (p1.x * r2 - p2.x * r1) / (r2 - r1)
    y = (p1.y * r2 - p2.y * r1) / (r2 - r1)

    return Point(x, y, name)

def pp_to_ray(p1, p2):
    rd = 0
    if p1.x == p2.x:
        rd = 90 if p2.y > p1.y else 270
    else:
        atan_value = (p2.y - p1.y) / (p2.x - p1.x)
        print(atan_value)
        rd = math.atan(atan_value) / math.pi * 180 \
                 if p2.x > p1.x else \
                 math.atan(atan_value) / math.pi * 180 + 180
        if rd < 0:
            rd += 360

    return Ray(p1, rd)

