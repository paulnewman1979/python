import random

def remainder():

    """divide remainder"""

    divisor_choices = [ 2, 3, 4, 5, 6, 7, 8, 9, 11 ]
    choice = random.randint(0, len(divisor_choices))
    divisor = divisor_choices[choice]
    if divisor == 11:
        dividend = random.randint(1000, 10000)
    else:
        dividend = random.randint(100, 500)
    expectedVal = dividend % divisor
    query = f"the remainder of {dividend} / {divisor} is\n"

    return (query, expectedVal)

