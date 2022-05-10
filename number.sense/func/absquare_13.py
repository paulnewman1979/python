import random

def square1():
    val1 = random.randint(11, 19)
    expectedVal = val1 * val1
    query = str(val1) + " * " + str(val1) + " = ?\n"
    return (query, expectedVal)

def aSquareBSquare1():
    t1 = random.randint(5, 19) * 5
    t2 = random.randint(1, 3)
    val1 = t1 - t2
    val2 = t1 + t2
    expectedVal = val1 * val2
    query = str(val1) + " * " + str(val2) + " = ?\n"
    return (query, expectedVal)


