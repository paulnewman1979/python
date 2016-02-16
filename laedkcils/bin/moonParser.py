#!/usr/bin/python

import urllib
import HTMLParser
import sys
from htmlentitydefs import entitydefs

class moonParser(HTMLParser.HTMLParser):
    inDealBox = False
    inProdImage = False
    inPostText = False
    inDealContent = False
    ACount = 0
    inStrong = False

    url = ""
    title = ""
    promo_hash = {}

    def __init__(self):
        self.promo_hash = {}
        HTMLParser.HTMLParser.__init__(self)
    
        self.inDealBox = False
        self.inProdImage = False
        self.inPostText = False
        self.inDealContent = False
        self.ACount = 0
        self.inStrong = False

    def handle_starttag(self, tag, attrs):
        url=""

        if tag == "a":
            self.inA = True
            for name, value in attrs:
                if name == 'href':
                    self.url = value
        elif tag == 'span':
            if self.inA:
                for name, value in attrs:
                    if name == 'class':
                        if value == 'img_wrap':
                            self.inImg = True
        elif tag == 'img':
            if self.inImg:
                for name, value in attrs:
                    if name == 'src':
                        self.prodImage = value
                    elif name == 'alt':
                        self.title = value
                        self.promo_hash[self.title] = []
                        self.promo_hash[self.title].append(self.url)
                        self.promo_hash[self.title].append(self.prodImage)

    def handle_endtag(self, tag):
        if tag == 'a':
            self.inA = False
            self.inImg = False

    def handle_data(self, data):
        if self.inDealContent and not self.inPostText and self.ACount == 2 and self.inStrong:
            self.title += data
        elif self.inDealContent and self.inPostText:
            self.content += data

    def handle_entityref(self, name):
        if entitydefs.has_key(name):
            self.handle_data(entitydefs[name]) 
        else: 
            self.handle_data('&'+name+';') 

if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf8')

    if len(sys.argv) < 2:
        print "usage: %s filename" % sys.argv[0]
    else:
        filename = sys.argv[1]
        input = open(filename, "r")
        html = input.read()
        input.close()
            
        parser = moonParser()
        parser.feed(html)
        for title in parser.promo_hash:
            print "%s\t%s\t%s" % (title, parser.promo_hash[title][0], parser.promo_hash[title][1])

