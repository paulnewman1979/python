from Point import Point
from Triangle import Triangle

class RightTriangle(Triangle):
    
    # define right triangle 
    def __init__(self, points = None, name = None):
        if points:
            self.points = points
        else:
            self.points = [
                Point(0, 0, name[0:1]),
                Point(400, 0, name[1:2]),
                Point(0, 250, name[2:3])
            ]


if __name__ == "__main__":

    rt = RightTriangle(None, "ABC")
    print(rt)
