import random

def add_dist():

    """add distibution"""

    nums = random.randint(3, 4)
    if nums == 3:
        val1 = random.randint(5, 10) * 10
        val3 = random.randint(5, val1)
        val1 = val1 - val3
        val2 = random.randint(10, 50)
        expectedVal = val1 + val2 + val3
        query = f"{val1} + {val2} + {val3} = \n"
    else:
        val1 = random.randint(5, 10) * 10
        val4 = random.randint(5, val1)
        val1 = val1 - val4

        val2 = random.randint(5, 10) * 10
        val3 = random.randint(5, val2)
        val2 = val2 - val3

        if random.randint(0, 2) == 1:
            val2, val3 = val3, val2

        expectedVal = val1 + val2 + val3 + val4
        query = f"{val1} + {val2} + {val3} + {val4} = \n"

    return (query, expectedVal)


def sub_dist():

    """sub distibution"""

    val2 = random.randint(5, 9) * 10
    val3 = random.randint(5, val2)
    val2 = val2 - val3
    val1 = random.randint(100, 200)
    expectedVal = val1 - val2 - val3
    query = f"{val1} - {val2} - {val3} = \n"

    return (query, expectedVal)

