import random
import copy

def add():
    """two number add"""
    val1 = random.randint(101, 199)
    val2 = random.randint(201, 399)
    expectedVal = val1 + val2
    query = str(val1) + " + " + str(val2) + " = ?\n"
    return (query, expectedVal)

def sub():
    """two number sub"""
    val2 = random.randint(100, 200)
    val1 = val2 + random.randint(200, 400)
    expectedVal = val1 - val2
    query = str(val1) + " - " + str(val2) + " = ?\n"
    return (query, expectedVal)

def mean():
    """mean value"""
    size = random.randint(4, 5)
    if size == 4:
        val1 = random.randint(10, 40)
        val2 = random.randint(10, 40)
        val3 = random.randint(10, 40)
        val4 = random.randint(10, 40) + val1 + val2 + val3
        val4 = (val4 // 4 + 1) * 4 - val1 - val2 - val3
        expectedVal = (val1 + val2 + val3 + val4) / 4
        query = f"the mean of the list {val1}, {val2}, {val3}, {val4} is\n"
    elif size == 5:
        val1 = random.randint(10, 40)
        val2 = random.randint(10, 40)
        val3 = random.randint(10, 40)
        val4 = random.randint(10, 40)
        val5 = random.randint(10, 40) + val1 + val2 + val3 + val4
        val5 = (val5 // 4 + 1) * 4 - val1 - val2 - val3 - val4
        expectedVal = (val1 + val2 + val3 + val4 + val5) / 5
        query = f"the mean of the list {val1}, {val2}, {val3}, {val4}, {val5} is\n"

    return (query, expectedVal)

def median():
    """median value"""
    size = random.randint(4, 5)
    if size == 4:
        val4 = random.randint(11, 48)
        val2 = random.randint(val4 + 1, 49)
        if (val2 + val4) % 2 == 1:
            val2 = val2 + 1
        val1 = random.randint(val2 + 1, 50)
        val3 = random.randint(10, val4)

        vals = [val1, val2, val3, val4]
        sortedVals = copy.deepcopy(vals)
        sortedVals.sort()
        print(sortedVals)
        expectedVal = (sortedVals[1] + sortedVals[2]) // 2
        query = f"the median of the list {vals[0]}, {vals[1]}, {vals[2]}, {vals[3]} is\n"
    elif size == 5:
        vals = [random.randint(10, 100),
                random.randint(10, 100),
                random.randint(10, 100),
                random.randint(10, 100),
                random.randint(10, 100)]
        sortedVals = copy.deepcopy(vals)
        sortedVals.sort()
        expectedVal = sortedVals[2]
        query = f"the median of the list {vals[0]}, {vals[1]}, {vals[2]}, {vals[3]}, {vals[4]} is\n"
    return (query, expectedVal)
