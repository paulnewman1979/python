#!/usr/bin/python

import json
import urllib
import HTMLParser
import sys
import re
import os
from htmlentitydefs import entitydefs

class myhabitParser(HTMLParser.HTMLParser):
    inPrice = False
    inPriceMSRP = False
    inProduct = False
    dirname =""
    smallImages = []

    url = ""
    tmpUrl = ""
    price = ""
    brand = ""
    product = ""
    msrp = ""
    discount = ""
    image = ""
    tmpUrl = ""
    tmpImage = ""

    productHash = {}

    def __init__(self):
        HTMLParser.HTMLParser.__init__(self)
        self.inPriceMSRP = False
        self.inPrice = False
        self.inProduct = False
        self.dirname = ""
        self.url = ""
        self.tmpUrl = ""
        self.productHash = {}
        self.smallImages = []

    def handle_starttag(self, tag, attrs):
        if tag == 'img':
            for name, value in attrs:
                if name == 'src':
                    self.tmpImage = value
                elif name == 'class':
                    if value == 'iImg af' or value == 'iImg cf' or value == 'iImg':
                        self.image = "%s/%s" % (self.dirname, self.tmpImage)
                     #print "DEBUG: image=%s" % self.image
        elif tag == 'span':
            for name, value in attrs:
                if name == 'class' and value == 'listprice':
                    self.inPriceMSRP = value
                elif name == 'class' and value == 'ourprice':
                    self.inPrice = True
        elif tag == 'a':
            isUrl = False
            for name, value in attrs:
                if name == 'class' and value == 'evt-prdtImg-a teenAsinImgLink':
                    isUrl = True
                elif name == 'href':
                    self.tmpUrl = value
            if isUrl:
                self.url = self.tmpUrl
                 #print "DEBUG: url=%s" % self.url
        elif tag == 'div':
            for name, value in attrs:
                if name == 'class' and value == 'title':
                    self.inProduct = True

    def handle_endtag(self, tag):
        if tag == 'span':
            if self.inPriceMSRP:
                self.inPriceMSRP = False
            elif self.inPrice:
                self.inPrice = False
        elif tag == 'div':
            if self.inProduct:
                self.inProduct = False

    def handle_data(self, data):
        if self.inPriceMSRP:
            self.msrp = data.strip().replace("$","").replace(",","")
             #print "DEBUG: msrp=%s" % self.msrp
        elif self.inPrice:
            self.price = data.strip().replace("$","").replace(",","")
             #print "DEBUG: price=%s" % self.price
            if self.url != "":
                self.productHash[self.url] = {}
                self.productHash[self.url]["brand"] = "Michael Kors"
                self.productHash[self.url]["product"] = self.product
                self.productHash[self.url]["image"] = self.image
                self.productHash[self.url]["price"] = self.price
                self.productHash[self.url]["msrp"] = self.msrp
                self.productHash[self.url]["soldout"] = 0
        elif self.inProduct:
            self.product = data
             #print "DEBUG: product=%s" % self.product

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
        dirname = os.path.dirname(filename)
        input = open(filename, "r")
        html = input.read()
        input.close()
            
        parser = myhabitParser()
        parser.dirname = dirname
        parser.feed(html)

        output = open(filename + ".json", "w")
        output.write(json.dumps(parser.productHash))
        output.close()
