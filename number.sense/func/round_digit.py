import random

def round_digit():
    """round"""
    value = random.randint(100, 9999)
    if value >= 1000:
        maxDigit = 4
    elif value >= 100:
        maxDigit = 3
    
    qDigit = random.randint(1, maxDigit - 1)
    if qDigit == 1:
        qDigit = "ten"
        expectedVal = round(int((value/10)+0.00001), 0) * 10
    elif qDigit == 2:
        qDigit = "hundred"
        expectedVal = round(int((value/100)+0.00001), 0) * 100
    else:
        qDigit = "thousand"
        expectedVal = round(((value/1000)+0.00001), 0) * 1000
    query = f"{value} rounded to the nearest {qDigit} is\n"
    return (query, expectedVal)

