#!/usr/local/bin/python

import sys
import os
import re

class dealSelector:
    ignoredTitle = {}

    ignoredWord = {}
    ignoredGroup = []
    ignoredInfo = []
    ignoredInfoUsedCount = {}

    desiredWord = {}
    desiredGroup = []

    filterRule = ""

    def __init__(self, ignoredInfoUsedCount=None):
        self.ignoredTitle = {}

        self.ignoredWord = {}
        self.ignoredGroup = []
        self.ignoredInfo = []

        self.desiredWord = {}
        self.desiredGroup = []
        self.ignoredInfoUsedCount = ignoredInfoUsedCount

        self.filterRule = ""

        conf = open("../conf/ignore.title.conf", "r")
        for line in iter(conf.readline, ''):
            line = line.rstrip()
            self.ignoredTitle[line] = 1
        conf.close()

        newCount = False if self.ignoredInfoUsedCount else True
        if newCount:
            self.ignoredInfoUsedCount = dict()

        conf = open("../conf/ignore.word.conf", "r")
        index = 0
        for line in iter(conf.readline, ''):
            if line[0:1] != '#':
                line = line.rstrip()
                line = line.lstrip()
                if line not in self.ignoredInfoUsedCount or newCount:
                    self.ignoredInfoUsedCount[line] = 0
                words = line.split(' ')
                self.ignoredGroup.append(len(words))
                self.ignoredInfo.append(line)
                for word in words:
                    if word not in self.ignoredWord:
                        self.ignoredWord[word] = [];
                    self.ignoredWord[word].append(index)
                index += 1
        conf.close()

        conf = open("../conf/desire.word.conf", "r")
        index = 0
        for line in iter(conf.readline, ''):
            if line[0:1] != '#':
                line = line.rstrip()
                line = line.lstrip()
                words = line.split(' ')
                self.desiredGroup.append(len(words))
                for word in words:
                    if not word in self.desiredWord:
                        self.desiredWord[word] = [];
                    self.desiredWord[word].append(index)
                index += 1
        conf.close()

    def checkDeal(self, title, enableDebug = False):
        if title in self.ignoredTitle:
            return False

        title = title.lower()
#        title = re.sub("[,/:();*+-@\[\]]", " ", title)
        title = title.replace(",", " ")
        title = title.replace("/", " ")
        title = title.replace(":", " ")
        title = title.replace("(", " ")
        title = title.replace(")", " ")
        title = title.replace(";", " ")
        title = title.replace("*", " ")
        title = title.replace("+", " ")
        title = title.replace("-", " ")
        title = title.replace("@", " ")
        title = title.replace("[", " ")
        title = title.replace("]", " ")
        title = title.replace("!", " ")
        title = re.sub("  *", " ", title)

        words = title.split(" ");

        if enableDebug:
            print(f"clean title = \"{title}\"")

        # desired word list
        indexCount = {}
        for word in words:
            if word in self.desiredWord:
                for index in self.desiredWord[word]:
                    if index in indexCount:
                        indexCount[index] += 1
                        if enableDebug:
                            print("%s %d" % (word, indexCount[index]))
                    else:
                        indexCount[index] = 1
                        if enableDebug:
                            print("%s 1" % word)
                
        for index in indexCount:
            if indexCount[index] >= self.desiredGroup[index]:
                return True;

        # ignored word list
        indexCount = {}
        sameWordCount = {}
        if enableDebug:
            print("DEBUG: title is \"%s\"" % title)
        for word in words:
            if enableDebug:
                print("DEBUG: check \"%s\"" % word)
            if word in self.ignoredWord:
                if enableDebug:
                    print("DEBUG: \"%s\" is in ignored word list" % word)
                    print("DEBUG: ignored phrase length is %i" % len(self.ignoredWord[word]))
                if word not in sameWordCount:
                    if enableDebug:
                        print("DEBUG: \"%s\" new word" % word)
                    for index in self.ignoredWord[word]:
                        if index in indexCount:
                            indexCount[index] += 1
                        else:
                            indexCount[index] = 1
                        if enableDebug:
                            print("DEBUG: \"%s\" in ignored phrase %i, count=%i" % (word, index, indexCount[index]))
                    sameWordCount[word] = 1
                else:
                    if enableDebug:
                        print("DEBUG: \"%s\" duplicate" % word)
                    sameWordCount[word] = 1

        if enableDebug:
            print("DEBUG: validation")
        for index in indexCount:
            if enableDebug:
                print("DEBUG: title = %s" % title)
                print("DEBUG: rule = %s" % self.ignoredInfo[index])
            if indexCount[index] >= self.ignoredGroup[index]:
                if enableDebug:
                    print("DEBUG: \"%i\" >= \"%i\"" % (indexCount[index], self.ignoredGroup[index]))
                    print("DEBUG: filtered by %i [%s]" % (index, self.ignoredInfo[index]))
                self.filterRule = self.ignoredInfo[index]
                if self.ignoredInfo[index] in self.ignoredInfoUsedCount:
                    self.ignoredInfoUsedCount[self.ignoredInfo[index]] += 1
                else:
                    self.ignoredInfoUsedCount[self.ignoredInfo[index]] = 1
                return False;
            else:
                if enableDebug:
                    print("DEBUG: \"%i\" < \"%i\"" % (indexCount[index], self.ignoredGroup[index]))

        return True;



if __name__ == '__main__':
    enableDebug = False
    if len(sys.argv) < 2:
        print("usage:")
    else:
        selector = dealSelector()
        title = sys.argv[1]
        if len(sys.argv) > 2:
            enableDebug = True
        if selector.checkDeal(title, enableDebug):
            print(title)
        else:
            print ("filtered by \"%s\"" % selector.filterRule)
