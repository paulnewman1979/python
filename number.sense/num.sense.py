import os
import random
import time
import sys
import inquirer
import signal
from inspect import getmembers, isfunction

sys.path.insert(0, './func')
import add_sub_01
import round_100_02
import mul_div_03
import remainder_04
import add_estimation_05
import digit_06
import add_sub_dist_08
import round_09
import square_cubic_power_10
import mul5_11
import absquare_13


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
        add_sub_01.add,
        add_sub_01.sub,
        add_sub_01.mean,
        add_sub_01.median,
        round_100_02.add100,
        round_100_02.sub100,
        mul_div_03.mul5,
        mul_div_03.mul100,
        remainder_04.remainder,
        add_estimation_05.add_estimation,
        digit_06.digit,
        add_sub_dist_08.add_dist,
        add_sub_dist_08.sub_dist,
        round_09.round_digit,
        square_cubic_power_10.power,
        mul5_11.mul5,
        absquare_13.aSquareBSquare1
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
            #if fun.__name__ == name:
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
            if (type(expectedVal) is list and value >= expectedVal[0] and value <= expectedVal[1]) or \
                    (type(expectedVal) is not list and value == expectedVal):
                print("Great Job")
        
        funLen = len(choiceFunArray)
        funIndex = random.randint(0, funLen - 1)
        fun = choiceFunArray[funIndex]
        (query, expectedVal) = fun()
        try:
            value = int(input("\n\n" + query))
        except:
            value = 1
        if testMode:
            if (type(expectedVal) is list and value >= expectedVal[0] and value <= expectedVal[1]) or \
                    (type(expectedVal) is not list and value == expectedVal):
                correct += 1
                cr.append((query, expectedVal, value)) 
            else:
                wrong += 1
                wr.append((query, expectedVal, value)) 
        else:
            if (type(expectedVal) is list and value >= expectedVal[0] and value <= expectedVal[1]) or \
                    (type(expectedVal) is not list and value == expectedVal):
                correct += 1
            else:
                wrong += 1
            while ((type(expectedVal) is list and (value < expectedVal[0] or value > expectedVal[1])) or \
                    (type(expectedVal) is not list and value != expectedVal)) and value != -1:
                try:
                    value = int(input("\n\ntry it again, " + query))
                except:
                    value = 1
        cur = int(time.time())

    score = correct * 5 - wrong * 4
    print(f"\n\ncorrect={correct} wrong={wrong} score={score}")
