import random
import common

def mul5():

    """?5 multiplication"""

    val1 = random.randint(1,4) * 10 + 5
    val2 = random.randint(11, 19)
    expectedVal = val1 * val2
    query = common.mul_expr(val1, val2)
    return (query, expectedVal)

def mul100():

    """mul round to hundreds"""

    val1 = random.randint(30, 99)
    val2 = random.randint(1, 2)
    expectedVal = val1 * (100 - val2)
    query = common.mul_expr(val1, val2)
    return (query, expectedVal)

