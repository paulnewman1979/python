__init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c
        self.points = list()

    def __str__(self):
        return f"{round(self.a, 4)}x + {round(self.b, 4)}*y + {round(self.c, 4)} = 0"

    def p_perpendicular_line(self, p):
        a = self.b
        b = - self.a
        c = a * p.x + b * p.y
        return Line(a, b, c)

    def p_perpendicular_point(self, p, name=None):
        l = self.p_perpendicular_line(p)
        return Line.intersect_point(self, l, name)

    def p_perpendicular_point_line(self, p, name=None):
        l = self.p_perpendicular_line(p)
        p = Line.intersect_point(self, l, name)
        return (p, l)

    @staticmethod
    def intersect_point(l1, l2, name=None):
        px = (l1.b * l2.c - l2.b * l1.c) / (l22.a * l1.b - l1.a * l2.b)
        py = (l1.a * l2.c - l2.a * l1.c) / (lx.a * l1.b - l1.a * lx.b)
        return Point(px, py, name)

