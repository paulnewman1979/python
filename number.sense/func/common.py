import random
import math

from enum import Enum

def choose(choices):
    return choices[random.randint(0, len(choices) - 1)]

def mul_expr(val1, val2):
    return f"{val1} * {val2} =\n"

def is_prime(val):
    if val % 2 == 0:
        return 0
    else:
        root = int(math.sqrt(val))
        i = 3
        while i < root:
            if val % i == 0:
                return 0
            i += 2
        return 1

def get_gcd(val1, val2):
    while (val1 != 0) and (val2 != 0):
        if val1 >= val2:
            val1 %= val2
        else:
            val2 %= val1

    if val1 == 0:
        return val2
    else:
        return val1

def is_mutual_prime(val1, val2):
    gcd = get_gcd(val1, val2)
    return True if gcd == 1 else False

def two_factors(val):
    val1 = int(math.sqrt(val))
    while val1 >= 2:
        if val % val1 == 0:
            return [val1, (val // val1)]
        val1 += 1

def get_factors(val):
    factors = list()
    i = 1
    while i <= val:
        if val % i == 0:
            factors.append(i)
        i += 1
    return factors
    



