import random
import copy

def add_sub():

    """regular add/sub"""

    expectedVal = 0
    query = ""
     
    if random.randint(0, 1) == 0:
        val1 = random.randint(101, 199)
        val2 = random.randint(201, 399)
        expectedVal = val1 + val2
        query = str(val1) + " + " + str(val2) + " = ?\n"
    else:
        val2 = random.randint(100, 200)
        val1 = val2 + random.randint(200, 400)
        expectedVal = val1 - val2
        query = str(val1) + " - " + str(val2) + " = ?\n"

    return (query, expectedVal)

