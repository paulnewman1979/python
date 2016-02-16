#!/usr/bin/python

import sys
import os
import re

class dealSelector:
    ignored_title = {}

    ignored_word = {}
    ignored_group = []
    ignored_info = []

    desired_word = {}
    desired_group = []

    filter_rule = ""

    def __init__(self):
        self.ignored_title = {}

        self.ignored_word = {}
        self.ignored_group = []
        self.ignored_info = []

        self.desired_word = {}
        self.desired_group = []

        self.filter_rule = ""

        conf = open("../conf/ignore.title.conf", "r")
        for line in iter(conf.readline, ''):
            line = line.rstrip()
            self.ignored_title[line] = 1
#            print "DEBUG: loading ignored title %s" % line
        conf.close()
#        print ""

        conf = open("../conf/ignore.word.conf", "r")
        index = 0
        for line in iter(conf.readline, ''):
            if line[0:1] != '#':
                line = line.rstrip()
                words = line.split(' ')
#                print "DEBUG: loading ignored words : %i [%s] %i" % (index, line, len(words))
                self.ignored_group.append(len(words))
                self.ignored_info.append(line)
                for word in words:
                    if word not in self.ignored_word:
                        self.ignored_word[word] = [];
                    self.ignored_word[word].append(index)
#                    print "DEBUG: loading %s %i" % (word, index)
                index += 1
        conf.close()
#        print ""

        conf = open("../conf/desire.word.conf", "r")
        index = 0
        for line in iter(conf.readline, ''):
            if line[0:1] != '#':
                line = line.rstrip()
#                print "DEBUG: loading desired words : %s" % line
                words = line.split(' ')
                self.desired_group.append(len(words))
                for word in words:
                    if not word in self.desired_word:
                        self.desired_word[word] = [];
                    self.desired_word[word].append(index)
                index += 1
        conf.close()
#        print ""

    def checkDeal(self, title):
        if title in self.ignored_title:
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

        words = title.split(" ");

        # desired word list
        index_count = {}
        for word in words:
            if word in self.desired_word:
                for index in self.desired_word[word]:
                    if index in index_count:
                        index_count[index] += 1
                    else:
                        index_count[index] = 1
                
        for index in index_count:
            if index_count[index] >= self.desired_group[index]:
                return True;

        # ignored word list
        index_count = {}
        for word in words:
            if word in self.ignored_word:
#                print "WHAT: word %s" % word
#                print "WHAT: len ignored_word %i" % len(self.ignored_word[word])
                for index in self.ignored_word[word]:
#                    print "WHAT: %i" % index
                    if index in index_count:
                        index_count[index] += 1
                    else:
                        index_count[index] = 1

        for index in index_count:
            if index_count[index] >= self.ignored_group[index]:
#                print "DEBUG : title = %s" % title
#                print "DEBUG : WHAT %i >= %i" % (index_count[index], self.ignored_group[index])
#                print "DEBUG: filtered by %i [%s]" % (index, self.ignored_info[index])
#                print "\tfiltered by %i [%s]" % (index, self.ignored_info[index])
                self.filter_rule = self.ignored_info[index]
                return False;

        return True;



if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "usage:"
    else:
        selector = dealSelector()
        title = sys.argv[1]
        if selector.checkDeal(title):
            print title
        else:
            print "filtered by %s" % selector.filter_rule
