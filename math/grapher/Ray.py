import math
from Point import Point
from Line import Line

class Ray:

    # define ray
    # from point p to direction
    def __init__(self, end_point, degree):
        self.end_point = end
        self.degree = degree

    def get_line(self):
        if self.degree == 90:
            a = 0
            b = 1
            c = -self.end_point.y
        elif self.degree == 270:
            a = 0
            b = -1
            c = self.end_point.y
        else:
            a = 1
            b = math.tan(self.degree)
            c = - a * self.rp.x - b * self.rp.y

        return Line(a, b, c)
