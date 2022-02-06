#!/usr/local/bin/python

import sys
import random

if __name__ == '__main__':
    gradeArr = list()
    termArr = list()
    with open('./performance.direction.txt', 'r') as fp:
        count = 0
        lastGrade = 1
        gradeArr.append(-1)
        for line in fp.readlines():
            arr = line.strip().split('\t')
            grade = (int)(arr[0])
            termArr.append(arr[1:])
            if grade != lastGrade:
                gradeArr.append(count)
                lastGrade = grade
            count = count + 1
        gradeArr.append(count - 1)
    fp.close()

    print(chr(27)+'[2j')
    print('\033c')
    print('\x1bc')

    inputstr = input('\n\nchoose your level, for example: 1-5, 2-2\n\n\n')
    (startLevel, endLevel) = inputstr.split('-')
    startLevel = int(startLevel)
    endLevel = int(endLevel)
    startPos = gradeArr[startLevel - 1] + 1
    endPos = gradeArr[endLevel]
    count = endPos - startPos + 1

    print(chr(27)+'[2j')
    print('\033c')
    print('\x1bc')

    retidx = 1
    correct = 0
    error = 0
    while retidx != 5:
        ques = random.randint(startPos, endPos)
        ans1 = random.randint(startPos, endPos)
        while termArr[ans1][0] == termArr[ques][0]:
            ans1 = random.randint(startPos, endPos)
        ans2 = random.randint(startPos, endPos)
        while termArr[ans2][0] == termArr[ques][0] or ans2 == ans1:
            ans2 = random.randint(startPos, endPos)
        ans3 = random.randint(startPos, endPos)
        while termArr[ans3][0] == termArr[ques][0] or ans3 == ans1 or ans3 == ans2:
            ans3 = random.randint(startPos, endPos)

        if len(termArr[ques]) > 2:
            idx = random.randint(1, len(termArr[ques]) - 1)
        else:
            idx = 1
        print(f'\n\n{termArr[ques][idx]} means:\n\n')
        anidx = random.randint(1, 4)
        if anidx == 1:
            print(f'1) {termArr[ques][0]}')
            print(f'2) {termArr[ans1][0]}')
            print(f'3) {termArr[ans2][0]}')
            print(f'4) {termArr[ans3][0]}')
        elif anidx == 2:
            print(f'1) {termArr[ans1][0]}')
            print(f'2) {termArr[ques][0]}')
            print(f'3) {termArr[ans2][0]}')
            print(f'4) {termArr[ans3][0]}')
        elif anidx == 3:
            print(f'1) {termArr[ans1][0]}')
            print(f'2) {termArr[ans2][0]}')
            print(f'3) {termArr[ques][0]}')
            print(f'4) {termArr[ans3][0]}')
        else:
            print(f'1) {termArr[ans1][0]}')
            print(f'2) {termArr[ans2][0]}')
            print(f'3) {termArr[ans3][0]}')
            print(f'4) {termArr[ques][0]}')
        retidx = int(input('\nyour choice is (5 to quit): '))
        print(chr(27)+'[2j')
        print('\033c')
        print('\x1bc')
        if retidx != 5:
            if retidx == anidx:
                correct = correct + 1
                print("           .---.                                                                            ,--,    ")
                print("          /. ./|                            ,---,                     .--.,               ,--.'|    ")
                print("      .--'.  ' ;   ,---.        ,---,     ,---.'|            __  ,-.,--.'  \         ,--, |  | :    ")
                print("     /__./ \ : |  '   ,'\   ,-+-. /  |    |   | :          ,' ,'/ /||  | /\/       ,'_ /| :  : '    ")
                print(" .--'.  '   \' . /   /   | ,--.'|'   |    |   | |   ,---.  '  | |' |:  : :    .--. |  | : |  ' |    ")
                print("/___/ \ |    ' '.   ; ,. :|   |  ,\"' |  ,--.__| |  /     \ |  |   ,':  | |-,,'_ /| :  . | '  | |    ")
                print(";   \  \;      :'   | |: :|   | /  | | /   ,'   | /    /  |'  :  /  |  : :/||  ' | |  . . |  | :    ")
                print(" \   ;  `      |'   | .; :|   | |  | |.   '  /  |.    ' / ||  | '   |  |  .'|  | ' |  | | '  : |__  ")
                print("  .   \    .\  ;|   :    ||   | |  |/ '   ; |:  |'   ;   /|;  : |   '  : '  :  | : ;  ; | |  | '.'| ")
                print("   \   \   ' \ | \   \  / |   | |--'  |   | '/  ''   |  / ||  , ;   |  | |  '  :  `--'   \;  :    ; ")
                print("    :   '  |--\"   `----'  |   |/      |   :    :||   :    | ---'    |  : \  :  ,      .-./|  ,   /  ")
                print("     \   \ ;              '---'        \   \  /   \   \  /          |  |,'   `--`----'     ---`-'   ")
                print("      '---\"                             `----'     `----'           `--'                            ")
            else:
                error = error + 1
                print(f"Incorrect, {termArr[ques][idx]} means {termArr[ques][0]}")

            print(f"\n\n\tcorrect = {correct}\n\terror   = {error}")




