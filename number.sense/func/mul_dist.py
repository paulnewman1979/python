import random
import copy
import common

def mul_dist():

    """multiplication distributive"""

    expectedVal = 0
    query = ""

    choice = random.randint(0, 3)
    if choice == 0: # val1 * 99
        val1 = random.randint(30, 99)
        val2 = 100 - random.randint(1, 3)
        if random.randint(0, 1) == 1:
            val1, val2 = val2, val1
        expectedVal = val1 * val2
        query = common.mul_expr(val1, val2)
    elif choice == 1: # val1 * val2 + val1
        val1 = random.randint(4, 9)
        val2 = random.randint(8, 15)
        choice1 = random.randint(0, 3)
        expectedVal = val1 * val2 + val1
        if choice1 == 0:
            query = f"{val1} * {val2} + {val1} =\n"
        elif choice1 == 1:
            query = f"{val2} * {val1} + {val1} =\n"
        elif choice1 == 2:
            query = f"{val1} + {val2} * {val1} =\n"
        else:
            query = f"{val1} + {val1} * {val2} =\n"
    elif choice == 2: # val1 * val2 - val1
        val1 = random.randint(4, 9)
        val2 = random.randint(8, 15)
        choice1 = random.randint(0, 1)
        expectedVal = val1 * val2 + val1
        if choice1 == 0:
            query = f"{val1} * {val2} - {val1} =\n"
        else:
            query = f"{val2} * {val1} - {val1} =\n"
    else:
        val1 = random.randint(6, 9)
        val2 = random.randint(4, 6) * 10
        val3 = val1 * 2
        val4 = random.randint(6, 19)
        val2 -= val4 * 2
        if random.randint(0, 1) == 1:
            val1, val2, val3, val4 = val3, val4, val1, val2
        if random.randint(0, 1) == 1:
            val1, val2 = val2, val1
        if random.randint(0, 1) == 1:
            val3, val4 = val4, val3
        expectedVal = val1 * val2 + val3 * val4
        query = f"{val1} * {val2} + {val3} * {val4} =\n"
        
    return (query, expectedVal)
