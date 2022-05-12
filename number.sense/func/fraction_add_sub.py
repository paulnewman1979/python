import random
import copy
import common

def fraction_add_sub():

    """fraction addition/subtraction"""

    expectedVal = 0
    query = ""
    r0 = 0
    r1 = 0
    r2 = 0

    choice = random.randint(0, 1)
    if choice == 0: # 1/a + 1/b or 1 - 1/a - 1/b
        val1 = random.randint(2, 9)
        val2 = random.randint(2, 9)
        while val2 == val1:
            val2 = random.randint(2, 9)

        if random.randint(0, 1) == 0:
            r1 = val1 + val2
            r2 = val1 * val2
            query = f"1/{val1} + 1/{val2} =\n"
        else:
            r2 = val1 * val2
            r1 = r2 - val1 + val2
            query = f"1 - 1/{val1} - 1/{val2} =\n"
    else: # 1/4 + 1/12 + 1/36
        val3 = random.randint(2,19) * 6
        factors = common.get_factors(val3)
        choice1 = random.randint(1, len(factors) - 2)
        choice2 = choice1
        while choice2 == choice1:
            choice2 = random.randint(1, len(factors) - 2)
        val1 = val3 / factors[choice1]
        val2 = val3 / factors[choice2]

        r1 = 1 + val3 // choice1 + val3 // choice2
        r2 = val3
        query = f"1/{val1} + 1/{val2} + 1/{val3} =\n"

    gcd = common.get_gcd(r1, r2)
    if gcd > 1:
        r1 /= gcd
        r2 /= gcd
    expectedVal = [r0, r1, r2]

    return (query, expectedVal)
