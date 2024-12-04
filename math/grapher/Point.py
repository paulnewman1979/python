class Point:
    
    # define point as
    # coordinator (x, y) and name
    def __init__(self, x, y, name):
        self.x = x
        self.y = y
        self.name = name

    def __str__(self):
        return f"{self.name} ({round(self.x, 4)}, {round(self.y, 4)})"

