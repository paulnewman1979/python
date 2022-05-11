import random
import common

def mul5():

    """multiply 5, 15, 25, 125, ..."""

    val1, val2, val3 = 0, 0, 0

    if random.randint(0, 1) == 1:

        choice = random.randint(0, 6)

        if choice == 0: # 5
            val1 = 5
            val2 = random.randint(21, 200)
        elif choice == 1: # 25
            val1 = 25
            val2 = random.randint(21, 200)
        elif choice == 2: # 125
            val1 = 125
            val2 = random.randint(21, 100)
        elif choice == 3: # 15
            val1 = 15
            val2 = random.randint(8, 20) * 2
        elif choice == 4: # 75
            val1 = 75
            val2 = random.randint(8, 20) * 4
        elif choice == 5: # 375, 625, 875
            choices = [375, 625, 875]
            val1 = common.choose(choices)
            val2 = random.randint(9, 20) * 8

        if random.randint(0, 2) == 1:
            val1, val2 = val2, val1
        expectedVal = val1 * val2
        query = f"{val1} * {val2} = \n"

    else:
        choice = random.randint(0, 0)

        if choice == 0: # 5
            val1 = 5
            val3 = random.randint(2, 20) * 4
            val2 = random.randint(3, 10)

        if random.randint(0, 1) == 1:
            val1, val3 = val3, val1
        expectedVal = val1 * val2 * val3
        query = f"{val1} * {val2} * {val3} = \n"

    return (query, expectedVal)

