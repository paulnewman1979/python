import random

def add100():
    val1 = random.randint(300, 500)
    val2 = random.randint(1, 3) * 100 - random.randint(1, 3)
    expectedVal = val1 + val2
    query = str(val1) + " + " + str(val2) + " = ?\n"
    return (query, expectedVal)

def sub100():
    val2 = random.randint(1, 3) * 100 - random.randint(1, 3)
    val1 = val2 + random.randint(100, 300)
    expectedVal = val1 - val2
    query = str(val1) + " - " + str(val2) + " = ?\n"
    return (query, expectedVal)


