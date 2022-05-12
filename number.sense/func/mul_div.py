import random
import common

def mul_div():

    """multiplication/division"""

    val1 = random.randint(1,4) * 10 + 5
    val2 = random.randint(11, 19)
    expectedVal = val1 * val2
    query = common.mul_expr(val1, val2)
    return (query, expectedVal)
