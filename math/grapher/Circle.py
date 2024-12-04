import math
from Line import Line
from Point import Point
import PointFunc
import Func

class Circle:

    def __init__(self, center, radius):
        self.center = center
        self.radius = radius

    def __str__(self):
        str = f"center " + self.center.__str__()
        str += f" radius {self.radius}"
        return str

    def p_tangent_ll(self, p):
        (p1, p2) = self.p_tangent_pp(p)
        return (PointFunc.pp_to_line(p, p1), PointFunc.pp_to_line(p, p2))

    def point_tangent_pp(self, p, names):
        cx = self.center.x
        cy = self.center.y
        cr = self.radius
        px = p.x
        py = p.y

        if (px - cx)**2 + (py - cy)**2 < cr**2:
            raise ValueError(f"tangent from point ({px}, {py} "\
                              "inside circle ({cx}, {cy}, {self.radius}")
        # (1)    (x-cx)^2 + (y-cy)^2 = cr^2 
        # (2)    (x-px)^2 + (y-py)^2 = (cx-px)^2 + (cy-py)^2 - cr^2
        # (1) - (2)
        # (3)    (px-cx)x + (py-cy)y = cr^2 - cx^2 - cy^2 + cx*px + cy*py
        #           t1         t2                     t3
        t1 = px - cx
        t2 = py - cy
        t3 = cr**2 - cx**2 - cy**2 + cx*px + cy*py

        # t1 = 0 and t2 = 0 can not be both true
        if t2 == 0:
            # (3) transform
            # (4)    t1(x - cx) = - t2*y - t1*cx + t3
            t4 = t1 * cx - t3
            a = t1**2 + t2**2
            b = - 2 * cy * t1**2 - 2 * t2 * t4
            c = (t1 * cy)**2 + t4**2 - cr**2
            (y1, y2) = Func.get_quadratic_roots(a, b, c)
            x1 = (t3 - t2 * y1) / t1
            x2 = (t3 - t2 * y2) / t1
            return (Point(x1, y1, names[0]), Point(x2, y2, names[1]))
        else:
            # (3) transform
            # (4)    t2(y - cy) = - t1*x - t2*cy + t3
            #                                t4
            # (1) * t2^2
            # (5)    (t2(x-cx))^2 + (t2(y-cy))^2 = (t2*cr)^2
            t4 = t2 * cy - t3
            a = t1**2 + t2**2
            b = 2 * (t1 * t4 - t2**2 * cx)
            c = (t2 * cx)**2 + t4**2 - (t2 * cr)**2
            (x1, x2) = Func.get_quadratic_roots(a, b, c)
            y1 = (t3 - t1 * x1) / t2
            y2 = (t3 - t1 * x2) / t2
            return (Point(x1, y1, names[0]), Point(x2, y2, names[1]))

    def point_tangent_ppll(self, p, names):
        (p1, p2) = self.point_tangent_pp(p, names)
        return (p1, p2, PointFunc.pp_to_line(p, p1), PointFunc.pp_to_line(p, p2))


if __name__ == "__main__":

    center = Point(0, 0, "O")
    radius = 5
    c1 = Circle(center, radius)
    p1 = Point(5, 5, "P")
    (t1, t2, l1, l2) = c1.point_tangent_ppll(p1, ["T1", "T2"])
    print(t1)
    print(t2)
    print(l1)
    print(l2)

