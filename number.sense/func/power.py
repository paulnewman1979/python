import random
import common

def power():

    """power"""

    choice = random.randint(0, 9)

    if choice == 0:
        choices = [11, 12, 13, 14, 15, 16, 17, 18, 19, 21, 22, 25, 32, 64]
        val = common.choose(choices)
        expectedVal = val * val
        query = f"{val}^2 = \n"
    elif choice == 1:
        choices = [11, 12, 13, 14, 15, 16, 17, 18, 19, 21, 22, 25]
        val1 = common.choose(choices)
        val2 = common.choose(choices)
        expectedVal = val1 * val1 + val2 * val2
        query = f"{val1}^2 + {val2}^2 =\n"
    elif choice == 2:
        choices = [4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
        val = common.choose(choices)
        expectedVal = 2 ** val
        query = f"2^{val} =\n"
    elif choice == 3:
        choices = [3, 4, 5, 6]
        val = common.choose(choices)
        expectedVal = 3 ** val
        query = f"3^{val} =\n"
    elif choice == 4:
        choices = [3, 4, 5]
        val = common.choose(choices)
        expectedVal = 5 ** val
        query = f"5^{val} =\n"
    elif choice == 4:
        choices = [3, 4, 5]
        val = common.choose(choices)
        expectedVal = 5 ** val
        query = f"5^{val} =\n"
    elif choice == 5: # like choice 2
        choices = [4, 5, 6, 7, 8, 9, 10, 11]
        val = common.choose(choices)
        val1 = random.randint(3, 5)
        val2 = val1 * 2
        val3 = val2 * 2
        expectedVal = val1 * (2 ** (val-1))
        query = f"The {val}th term in the geometric sequence {val1},{val2},{val3},... is\n"
    elif choice == 6: # like choice 3
        choices = [4, 5, 6, 7]
        val = common.choose(choices)
        val1 = random.randint(3, 5)
        val2 = val1 * 3
        val3 = val2 * 3
        expectedVal = val1 * (3 ** (val-1))
        query = f"The {val}th term in the geometric sequence {val1},{val2},{val3},... is\n"
    elif choice == 7:
        choices = [3, 4, 5, 6]
        val = common.choose(choices)
        expectedVal = 4 ** val
        query = f"4^{val} =\n"
    elif choice == 8:
        choices = [2, 3]
        val = common.choose(choices)
        expectedVal = 9 ** val
        query = f"9^{val} =\n"
    elif choice == 9:
        choices = [2, 3, 4]
        val = common.choose(choices)
        expectedVal = 8 ** val
        query = f"8^{val} =\n"

    return (query, expectedVal)

