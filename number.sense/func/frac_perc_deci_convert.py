import random
import common

def frac_perc_deci_convert():

    """fraction/percentage/decimal convertion"""

    expectedVal = 0
    query = ""
    r0 = 0
    r1 = 0
    r2 = 0

    choice = random.randint(0, 2)
    if choice == 0: # (a b/c)% -> fraction
        numerator = random.randint(3, 18) * 5
        denominator = numerator
        while not common.is_mutual_prime(numerator, denominator):
            denominator = random.randint(1, 5) * 2 + 1
        c = denominator
        a = numerator // c
        b = numerator % c

        r1 = numerator // 5
        r2 = denominator * 20
        gcd = common.get_gcd(r1, r2)
        if gcd > 1:
            r1 /= gcd
            r2 /= gcd
        expectedVal = [r0, r1, r2]
        query = f"({a} {b}/{c})% = (fraction)\n"
    elif choice == 1: # a/b = %
        factors = common.get_factors(100)
        factorChoice = random.randint(1, len(factors) - 2)
        b = factors[factorChoice]
        a = random.randint(1, b - 1)
        while not common.is_mutual_prime(a, b):
            a = random.randint(1, b - 1)
        expectedVal = a * 100 // b
        query = f"{a}/{b} = ?%\n"
    elif choice == 2: # 0.abcbcbcbc -> fraction
        if random.randint(0, 1) == 0: # with 0.a
            a = random.randint(1, 9)
            if random.randint(0, 1) == 0: # 1 digit repeat
                b = random.randint(1, 9)
                r1 = a * 10 + b
                r2 = 90
                gcd = common.get_gcd(r1, r2)
                r1 /= gcd
                r2 /= gcd
                expectedVal = [r0, r1, r2]
                query = f"0.{a}{b}{b}{b}{b}.... = (fraction)\n"
            else: # 2 digits repeat
                b = random.randint(1, 9)
                c = random.randint(1, 9)
                while c == b:
                    c = random.randint(1, 9)
                r1 = a * 99 + 10 * b + c
                r2 = 990
                gcd = common.get_gcd(r1, r2)
                r1 /= gcd
                r2 /= gcd
                expectedVal = [r0, r1, r2]
                query = f"0.{a}{b}{c}{b}{c}{b}{c}.... = (fraction)\n"
        else: # without 0.a
            if random.randint(0, 1) == 0: # 1 digit repeat
                b = random.randint(1, 8)
                r1 = b
                r2 = 9
                expectedVal = [r0, r1, r2]
                query = f"0.{b}{b}{b}{b}{b}.... = (fraction)\n"
            else: # 2 digits repeat
                b = random.randint(1, 9)
                c = random.randint(1, 9)
                while c == b:
                    c = random.randint(1, 9)
                r1 = 10 * b + c
                r2 = 99
                gcd = common.get_gcd(r1, r2)
                r1 /= gcd
                r2 /= gcd
                expectedVal = [r0, r1, r2]
                query = f"0.{b}{c}{b}{c}{b}{c}{b}{c}.... = (fraction)\n"
    else: # fraction to decimal, reciprocal of a/b
        factors = common.get_factors(100)
        factorChoice = random.randint(1, len(factors) - 2)
        a = factors[factorChoice]
        b = random.randint(a + 1, a * 5 - 1)
        while not common.is_mutual_prime(a, b):
            b = random.randint(a + 1, a * 5 - 1)
        expectedVal = b / a
        query = f"The reciprocal of {a}/{b} = (decimal)\n"

    return (query, expectedVal)

