import random
import common

def gcd_lcm():

    """gcd lcm"""

    gcd_choices = [ 3, 4, 5, 6, 7, 8, 9 ]
    gcd, val1, val2 = 2, 1, 1
    while gcd != 1:
        val1 = random.randint(3, 13)
        val2 = random.randint(3, 9)
        gcd = common.get_gcd(val1, val2)
       
    val = common.choose(gcd_choices)
    val1 *= val
    val2 *= val
    expectedVal = 0
    if random.randint(0, 1) == 0: # gcd
        expectedVal = val
        query = f"The GCD of {val1} and {val2} is\n"
    else: # lcm
        expectedVal = val1 // val * val2
        query = f"The LCM of {val1} and {val2} is\n"

    return (query, expectedVal)

