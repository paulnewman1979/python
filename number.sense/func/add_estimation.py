import random

def add_estimation():

    """add estimation"""

    choice = random.randint(3, 4)
    if choice == 3:
        val1 = random.randint(1000, 4000)
        val2 = random.randint(1000, 4000)
        val3 = random.randint(1000, 4000)
        expectedVal1 = (val1 // 100) * 100 + (val2 // 100) * 100 + (val3 // 100) * 100
        expectedVal2 = expectedVal1 + 300
        query = f"(estimate) {val1} + {val2} + {val3}\n"
    else:
        val1 = random.randint(100, 400)
        val2 = random.randint(100, 400)
        val3 = random.randint(100, 400)
        val4 = random.randint(100, 400)
        expectedVal1 = (val1 // 10) * 10 + (val2 // 10) * 10 + (val3 // 10) * 10 + (val4 // 10) * 10
        expectedVal2 = expectedVal1 + 40
        query = f"(estimate) {val1} + {val2} + {val3} + {val4}\n"

    return (query, [expectedVal1, expectedVal2])

