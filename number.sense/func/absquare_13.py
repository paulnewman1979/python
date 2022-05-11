import random
import common

def absquare():

    """ a^2-b^2 = (a-b)*(a+b) """

    choice = random.randint(0, 2)

    expectedVal = 0
    print(f"choice={choice}")
    query = ""
    if choice == 0:
        t1 = random.randint(5, 19) * 5
        t2 = random.randint(0, 3)
        val1 = t1 - t2
        val2 = t1 + t2
        expectedVal = val1 * val2
        query = common.mul_expr(val1, val2)
    elif choice == 1:
        unit = random.randint(1, 9)
        val1 = random.randint(1, 4) * 10 + unit
        val2 = val1 + random.randint(1, 4) * 10
        expectedVal = val2 * val2 - val1 * val1
        query = f"{val2}^2 - {val1}^2 =\n"
    elif choice == 2:
        t1 = random.randint(1, 3) * 10 + 1000
        t2 = random.randint(1, 3)
        val1 = t1 - t2
        val2 = t1 + t2
        expectedVal = val1 * val2
        query = common.mul_expr(val1, val2)

    return (query, expectedVal)


