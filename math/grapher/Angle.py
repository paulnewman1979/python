from Point import Point
from Ray import Ray

class Angel:

    #define angle

    def __init__(self, ray1, ray2)
        assert(ray1.end_point == ray2.end_point, f"{ray1} {ray2) different endpoint")
        self.ray1 = ray1
        self.ray2 = ray2
        self.degree = ray2.degree - ray1.degree
        if self.degree < 0:
            self.degree += 360

    def bisector_ray(self):
        degree = self.degree / 2 + self.ray1.degree
        if degree > 360:
            degree -= 360
        return Ray(self.endpoint, degree)

    def bisector_line(self):
        ray = self.bisector_ray()
        return ray.get_line()

