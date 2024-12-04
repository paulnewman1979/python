from Point import Point

class Triangle:
    
    # difine triangle with 3 vertices
    def __init__(self, points = None, name = None):
        if points:
            self.points = points
        else:
            self.points = [
                Point(0, 0, name[0:1]),
                Point(400, 0, name[1:2]),
                Point(125, 300, name[2:3])
            ]

    def __str__(self):
        return "triangle " + \
               ("".join([p.name for p in self.points])) + \
               "\t" + \
               (" ".join([f"({p.x}, {p.y})" for p in self.points]))

