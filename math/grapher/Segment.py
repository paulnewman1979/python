import PointFunc
from Line import Line

class Segment:
    
    # point a and b
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __str__(self):
        return f"{self.a.name}{self.b.name} " \
               f"({round(self.a.x, 4)}, {round(self.a.y, 4)}) to " \
               f"({round(self.b.x, 4)}, {round(self.b.y, 4)})"

    def line(self):
        a = self.b.y - self.a.y
        b = self.a.x - self.b.x
        c = - a * self.a.x - b * self.a.y
        return Line(a, b, c)

    def midpoint(self):
        return PointFunc.pp_to_p_inner(self.b, 1, 1)

    def perpendicular_bisector_line(self):
        midpoint = self.midpoint()
        line = self.line()
        return line.p_perpendicular_line(midpoint)

