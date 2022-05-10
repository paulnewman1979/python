import random

def add():
    val1 = random.randint(100, 200)
    val2 = random.randint(200, 400)
    expectedVal = val1 + val2
    query = str(val1) + " + " + str(val2) + " = ?\n"
    return (query, expectedVal)

def sub():
    val2 = random.randint(100, 200)
    val1 = val2 + random.randint(200, 400)
    expectedVal = val1 - val2
    query = str(val1) + " - " + str(val2) + " = ?\n"
    return (query, expectedVal)

def mean():

    size = random.randint(4, 5)
    if size == 4:
        val1 = random.randint(10, 40)
        val2 = random.randint(10, 40)
        val3 = random.randint(10, 40)
        val4 = random.randint(10, 40) + val1 + val2 + val3
        val4 = (val4 // 4 + 1) * 4 - val1 - val2 - val3
        expectedVal = (val1 + val2 + val3 + val4) / 4
        query = f"the mean of the list {val1}, {val2}, {val3}, {val4} is"
    elif size == 5:
        val1 = random.randint(10, 40)
        val2 = random.randint(10, 40)
        val3 = random.randint(10, 40)
        val4 = random.randint(10, 40)
        val5 = random.randint(10, 40) + val1 + val2 + val3 + val4
        val5 = (val5 // 4 + 1) * 4 - val1 - val2 - val3 - val4
        expectedVal = (val1 + val2 + val3 + val4 + val5) / 5
        query = f"the mean of the list {val1}, {val2}, {val3}, {val4}, {val5} is"

    return (query, expectedVal)

def median():

    size = random.randint(4, 5)
    if size == 4:
        val1 = random.randint(10, 30)
        val2 = random.randint(10, 30)
        val3 = random.randint(10, 30)
        val4 = random.randint(10, 30) + val1 + val2 + val3
        val4 = (val4 // 4 + 1) * 4 - val1 - val2 - val3
        expectedVal = (val1 + val2 + val3 + val4) / 4
        query = f"the mean of the list {val1}, {val2}, {val3}, {val4} is"
    elif size == 5:
        val1 = random.randint(10, 30)
        val2 = random.randint(10, 30)
        val3 = random.randint(10, 30)
        val4 = random.randint(10, 30)
        val5 = random.randint(10, 30) + val1 + val2 + val3 + val4
        val5 = (val5 // 4 + 1) * 4 - val1 - val2 - val3 - val4
        expectedVal = (val1 + val2 + val3 + val4 + val5) / 5
        query = f"the mean of the list {val1}, {val2}, {val3}, {val4}, {val5} is"

    return (query, expectedVal)
