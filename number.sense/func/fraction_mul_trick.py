import random
import common

def fraction_mul_trick():

    """fraction mul trick"""

    expectedVal = 0
    query = ""
    r0 = 0
    r1 = 0
    r2 = 0

    choice = random.randint(0, 1)
    if choice == 0: # (a c/b) * (a (b-c)/b)
        a = random.randint(3, 9)
        b = random.randint(3, 8)
        c = random.randint(1, b - 1)
        gcd = common.get_gcd(b, c)
        if gcd > 1:
            b //= gcd
            c //= gcd
        bmc = b - c
        query = f"({a} {c}/{b}) * ({a} {bmc}/{b}) =\n"
        r1 = c * bmc
        r2 = b * b
        r0 = a * a + a + (r1 // r2)
        r1 %= r2
    else: # (a c/d) * (b c/d) and (a+b)===0 (d)
        d = random.randint(3, 8)
        absum = random.randint(2, 4) * d
        a = d
        while not common.is_mutual_prime(a, d):
            a = random.randint(d + 1, absum - 1)
        b = absum - a
        c = random.randint(1, d - 1)

        query = f"({a} {c}/{d}) * ({b} {c}/{d}) =\n"
        r2 = d * d
        r1 = c * c
        r0 = a * b + (a + b) * c // d

    expectedVal = [r0, r1, r2]

    return (query, expectedVal)

