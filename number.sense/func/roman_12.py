import random
import common

def roman():

    """roman number"""

    roman_dict = {
            "I":1,
            "V":5,
            "X":10,
            "L":50,
            "C":100,
            "D":500,
            "M":1000
            }

    mapping = [
            ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX"],
            ["X", "XX", "XXX", "XL", "L", "LX", "LXX", "LXXX", "XC"],
            ["C", "CC", "CCC", "CD", "D", "DC", "DCC", "DCCC", "CM"],
            ["M", "MM", "MMM", "",   "",  "",   "",    "",     ""  ],
            ]

    val = random.randint(100, 2999)
    expectedVal = val
    qQuery = ""
    if val // 1000 > 0:
        qQuery += mapping[3][(val // 1000) - 1]
    val = val % 1000
    if val // 100 > 0:
        qQuery += mapping[2][(val // 100) - 1]
    val = val % 100
    if val // 10 > 0:
        qQuery += mapping[1][(val // 10) - 1]
    val = val % 10
    if val > 0:
        qQuery += mapping[0][val - 1]
    query = f"{qQuery} in Arabic Numerals is\n"

    return (query, expectedVal)

