import random

def square():
    val1 = random.randint(11, 19)
    expectedVal = val1 * val1
    query = str(val1) + " * " + str(val1) + " = ?\n"
    return (query, expectedVal)

