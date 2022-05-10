import os
import random

if __name__ == "__main__":
    value = -1
    expectedVal = 0
    while value != 0:
        print(chr(27)+"[2j")
        print("\033c")
        print("\x1bc")
        if value == expectedVal:
            print("\n\n\nGreat Job\n\n\n")

        val1 = random.randint(2, 10)
        val2 = random.randint(2, 10)
        expectedVal = val1 * val2
        try:
            value = input("\n\n" + str(val1) + " x " + str(val2) + " = ?\n")
        except:
            value = expectedValue - 1
        while value != expectedVal and value != 0:
            print(chr(27)+"[2j")
            print("\033c")
            print("\x1bc")
            try:
                value = input("\n\ntry it again, " + str(val1) + " x " + str(val2) + " = ?\n")
            except:
                value = expectedValue - 1
