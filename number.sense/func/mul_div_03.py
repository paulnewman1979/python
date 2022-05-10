import random

def mul1():
    val1 = random.randint(2, 11)
    val2 = random.randint(2, )
    expectedVal = val1 * (100 - val2)
    query = str(val1) + " x " + str(100 - val2) + " = ?\n"
    return (query, expectedVal)

def mul100():
    val1 = random.randint(30, 99)
    val2 = random.randint(1, 2)
    expectedVal = val1 * (100 - val2)
    query = str(val1) + " x " + str(100 - val2) + " = ?\n"
    return (query, expectedVal)

def mul5():
    val1 = random.randint(1,4) * 10 + 5
    val2 = random.randint(11, 19)
    expectedVal = val1 * val2
    query = str(val1) + " x " + str(val2) + " = ?\n"
    return (query, expectedVal)


