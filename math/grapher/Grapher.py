from Point import Point
from Ray import Ray
from Pentagon import Pentagon
from Circle import Circle
from Triangle import Triangle
from RightTriangle import RightTriangle

class Grapher:

    def __init__(self):
        self.points = list()
        self.segments = list()
        self.circles = list()

    def construct(self):
        a = Point(0, 0, "A")
        self.points.append(a)
        d = Point(400, 100, "D")
        Ray

    def __str__(self):
        print(self.points)
        print(self.segments)
        print(self.circles)
