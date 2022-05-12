import random
import common

def mul_div_estimation():

    """multiplication/division estimation"""

    expectedVal = [0, 0]
    query = ""

    choice = random.randint(0, 1)
    if choice == 0: # 1/7 trick
        val1 = int((random.randint(1, 6) / 7) * 1000000)
        val2 = random.randint(2, 9)
        expectedVal = [val1 * val2, val1 * val2]
        query = common.mul_expr(val1, val2)
    elif choice == 1:
        newVal1 = random.randint(1, 9) * 50
        val1 = newVal1 + (1 if random.randint(0, 1) == 0 else -1)
        val2 = random.randint(200, 400)
        expectedVal = [(newVal1 - 1) * val2, (newVal1 + 1) * val2]
        
    return (query, expectedVal)

