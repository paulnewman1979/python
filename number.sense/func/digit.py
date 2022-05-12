import random

def digit():
    """digit"""
    value = random.randint(100, 10000)
    if value >= 1000:
        maxDigit = 3
    elif value >= 100:
        maxDigit = 2
    
    qDigit = random.randint(0, maxDigit)
    if qDigit == 0:
        qDigit = "units"
        expectedVal = value % 10
    elif qDigit == 1:
        qDigit = "tens"
        expectedVal = (value % 100) // 10
    elif qDigit == 2:
        qDigit = "hundreds"
        expectedVal = (value % 1000) // 100
    else:
        qDigit = "thousands"
        expectedVal = value // 1000
    query = f"the {qDigit} digit of {value} is\n"
    return (query, expectedVal)

