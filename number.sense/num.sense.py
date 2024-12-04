import os
import random
import time
import sys
import inquirer
import signal
from inspect import getmembers, isfunction

sys.path.insert(0, './func')
import add_sub
import add_sub_dist
import add_estimation
import add_sub_round
import mul_div
import mul_div_estimation
import mul_dist
import mul_5
import remainder
import fraction_compare
import fraction_add_sub
import fraction_mul_trick
import frac_perc_deci_convert
import power
import absquare
import digit
import round_digit
import roman
import gcd_lcm
import mean_median


if __name__ == "__main__":

    expectedVal = 0
    value = 2
    testMode = True
    while value != 1 and value != 0:
        value = int(input("\n\ntest mode or not, 1 means yes, 0 means no\n"))
        if value == 1:
            testMode = True
        elif value == 0:
            testMode = False

    testTime = 600
    value = 11
    while value < 1 or value > 10:
        value = int(input("\n\nhow long do you want to test, (1 - 10) minutes\n"))

    funArray = [
        add_sub.add_sub,
        add_sub_dist.add_sub_dist,
        add_estimation.add_estimation,
        add_sub_round.add_sub_round,
        mul_div.mul_div,
        mul_div_estimation.mul_div_estimation,
        mul_dist.mul_dist,
        mul_5.mul_5,
        remainder.remainder,
        fraction_compare.fraction_compare,
        fraction_add_sub.fraction_add_sub,
        fraction_mul_trick.fraction_mul_trick,
        frac_perc_deci_convert.frac_perc_deci_convert,
        power.power,
        absquare.absquare,
        digit.digit,
        round_digit.round_digit,
        roman.roman,
        gcd_lcm.gcd_lcm,
        mean_median.mean_median,
    ]
    #funArrayNames = [ fun.__name__ for fun in funArray ]
    funArrayNames = [ fun.__doc__ for fun in funArray ]
    funArrayNames.insert(0, "all")
    questions = [inquirer.Checkbox(
        'interests',
        message="What are you interested in?",
        choices=funArrayNames
    )]
    answers = inquirer.prompt(questions)  # returns a dict

    choiceFunArray = list()
    if len(answers["interests"]) == 0:
        answers["interests"].append("all")
    for fun in funArray:
        for name in answers["interests"]:
            if name == "all" or fun.__doc__ == name:
                choiceFunArray.append(fun)

    correct = 0
    wrong = 0
    cr = list()
    wr = list()

    cur = int(time.time())
    end = cur + 600
    while cur < end and value != -1:
        if not testMode:
            if (type(expectedVal) is list and \
                    ((len(expectedVal) == 2 and value >= expectedVal[0] and value <= expectedVal[1]) or \
                     (len(expectedVal) == 3 and value[0] == expectedVal[0] and value[1] == expectedVal[1] and value[2] == expectedVal[2])) \
                ) or \
                (type(expectedVal) is not list and value == expectedVal):
                print("Great Job")
        
        funLen = len(choiceFunArray)
        funIndex = random.randint(0, funLen - 1)
        fun = choiceFunArray[funIndex]
        (query, expectedVal) = fun()
        #print(f"expectedVal={expectedVal}")
        try:
            strValue = input("\n\n" + query)
            pos1 = strValue.find("/")
            if pos1 != -1: # fraction
                pos2 = strValue.find(" ")
                if pos2 != -1: # with whole number
                    value = [int(strValue[0:pos2]),
                            int(strValue[pos2 + 1:pos1]),
                            int(strValue[pos1 + 1:])]
                else:
                    value = [0,
                            int(strValue[0:pos1]),
                            int(strValue[pos1+1:])]
            else:
                pos1 = strValue.find(".")
                if pos1 != -1:
                    value = float(strValue)
                else:
                    value = int(strValue)
        except:
            value = 1
        print(f"value={value}")
        if testMode:
            if (type(expectedVal) is list and 
                    ((len(expectedVal) == 2 and value >= expectedVal[0] and value <= expectedVal[1]) or \
                     (len(expectedVal) == 3 and value[0] == expectedVal[0] and value[1] == expectedVal[1] and value[2] == expectedVal[2])) \
                ) or \
                (type(expectedVal) is not list and value == expectedVal):
                correct += 1
                cr.append((query, expectedVal, value)) 
            else:
                wrong += 1
                wr.append((query, expectedVal, value)) 
        else:
            if (type(expectedVal) is list and \
                    ((len(expectedVal) == 2 and value >= expectedVal[0] and value <= expectedVal[1]) or \
                     (len(expectedVal) == 3 and value[0] == expectedVal[0] and value[1] == expectedVal[1] and value[2] == expectedVal[2]))
                ) or \
                (type(expectedVal) is not list and value == expectedVal):
                correct += 1
            else:
                wrong += 1
            while not ((type(expectedVal) is list and \
                    ((len(expectedVal) == 2 and value >= expectedVal[0] and value <= expectedVal[1]) or \
                     (len(expectedVal) == 3 and value[0] == expectedVal[0] and value[1] == expectedVal[1] and value[2] == expectedVal[2]))
                ) or \
                (type(expectedVal) is not list and (value == expectedVal or value == -1))):
                print(f"expectedVal={expectedVal}")
                print(f"value={value}")
                try:
                    strValue = input("\n\ntry it again, " + query)
                    pos1 = strValue.find("/")
                    if pos1 != -1: # fraction
                        pos2 = strValue.find(" ")
                        if pos2 != -1: # with whole number
                            value = [int(strValue[0:pos2]),
                                    int(strValue[pos2 + 1:pos1]),
                                    int(strValue[pos1 + 1:])]
                        else:
                            value = [0,
                                    int(strValue[0:pos1]),
                                    int(strValue[pos1+1:])]
                    else:
                        pos1 = strValue.find(".")
                        if pos1 != -1:
                            value = float(strValue)
                        else:
                            value = int(strValue)
                    print(f"value={value}")
                except:
                    value = 1
        cur = int(time.time())

    score = correct * 5 - wrong * 4
    print(f"\n\ncorrect={correct} wrong={wrong} score={score}")
