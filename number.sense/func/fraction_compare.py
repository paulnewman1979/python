import random
import common

def fraction_compare():

    """fraction compare"""

    two_composite = False
    while not two_composite:
        two_composite = True
        val1 = random.randint(2, 50) * 2
        choice = random.randint(0, 1)
        val2 = val1 - 1 if choice == 0 else val1 + 1
        if common.is_prime(val2):
            two_composite = True
        if not two_composite:
            val2 = val1 + 1 if choice == 0 else val - 1
            if common.is_prime(val2):
                two_composite = True
    val1, val3 = common.two_factors(val1)
    val2, val4 = common.two_factors(val2)

    if random.randint(0, 1) == 0: # larger
        expectedVal = [0, val1, val2] if (val1 * val3) > (val2 * val4) \
                else [0, val4, val3]
        query = f"The larger of {val1}/{val2} and {val4}/{val3} is (fraction)\n"
    else:
        expectedVal = [0, val4, val3] if (val1 * val3) > (val2 * val4) \
                else [0, val1, val2]
        query = f"The lesser of {val1}/{val2} and {val4}/{val3} is (fraction)\n"

    return (query, expectedVal)

