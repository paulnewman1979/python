import math

def get_quadratic_roots(a, b, c):
    t1 = b**2 - 4 * a * c
    if t1 < 0:
        raise ValueError(f"b^2-4ac={t1} < 0")
    t2 = math.sqrt(t1)
    x1 = (-b + t2) / (2 * a)
    x2 = (-b - t2) / (2 * a)
    return (x1, x2)
