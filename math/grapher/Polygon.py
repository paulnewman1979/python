import math
from Point import Point
from Segment import Segment

class Polygon:

    def __init__(self, name, side_length):
        self.name = name
        n = len(name)
        x = 0
        y = 0
        self.points = list()
        self.segments = list()
        self.points.append(Point(0, 0, name[0]))

        d = 360 * math.pi / n
        cur_d = math.pi
        for i in range(1, n):
            cur_d -= d
            x += math.cos(d) * side_length
            y += math.sin(d) * side_length
            self.points.append(Point(x, y, name[i]))
            self.segments.append(Segment(self.points[i-1], self.points[i]))
        self.segments.append(Segment(self.points[n - 1], self.points[0]))

    def __str__(self):
        str = f"{self.name}\t"
        for point in self.points:
            str += "\t" + point.__str__()
        return str

    def get_points_segments(self):
        return (self.points, self.segments)

if __name__ == "__main__":

     square = Polygon("ABCD", 20)
     print(square)
