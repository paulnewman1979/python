#!/usr/bin/python

import json
import urllib
import HTMLParser
import sys
import re
import os
from htmlentitydefs import entitydefs

class coachoutletParser(HTMLParser.HTMLParser):
    inGridContainer = False
    inItemBox = False
    inItemText = False
    inPriceBox = False
    inPrice = False
    inDiscount = False
    inMSRP = False
    inPriceSavings = False
    inPriceMSRP = False
    inLi = False
    soldout = 0
    dirname =""
    smallImages = []

    url = ""
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
        self.inGridContainer = False
        self.inItemBox = False
        self.inItemText = False
        self.inPriceBox = False
        self.inDiscount = False
        self.inMSRP = False
        self.inPriceSavings = False
        self.inPriceMSRP = False
        self.inPrice = False
        self.inLi = False
        self.soldout = 0
        self.dirname = ""
        self.productHash = {}
        self.smallImages = []

    def handle_starttag(self, tag, attrs):
        if tag == 'li':
            for name, value in attrs:
                if name == 'class':
                    if value == 'list-item-first list-item box item' or value == 'list-item box item' or value == 'list-item box item ':
                        self.inLi = True
        elif tag == 'div':
            for name, value in attrs:
                if name == 'class':
                    if value == 'grid-container':
                        self.inGridContainer = True
                    elif value == 'item-text':
                        self.inItemText = True
                    elif value == 'price-box price-mode-three-tier':
                        self.inPriceBox = True
                    elif value == 'price-savings':
                        self.inPriceSavings = True
                    elif value == 'out-of-stock':
                        self.soldout = 1
        elif tag == 'p':
            for name, value in attrs:
                if name == 'class':
                    if value == 'price price-final':
                        self.inPriceSavings = True
                    elif value == 'price price-mfsrp ':
                        self.inPriceBox = True
        elif tag == 'img':
            if self.inGridContainer:
                inMainImage = True
                for name, value in attrs:
                    if name == 'class':
                        if value == 'main-image':
                            inMainImage = True
                        elif value == 'alt-image':
                            inMainImage = False
                    elif name == 'src':
                        if inMainImage:
                            self.image = "%s/%s" % (self.dirname, value)
                             #print "DEBUG: image=%s" % self.image
                        else:
                            image = "%s/%s" % (self.dirname, value)
                            self.smallImages.append(image)
                             #print "DEBUG: smallimage=%s" % image
        elif tag == 'a':
            if self.inItemText:
                for name, value in attrs:
                    if name == 'href':
                        self.url = value
                    elif name == 'title':
                        self.product = value
                         #print "DEBUG: product=%s" % self.product
        elif tag == 'span':
            if self.inPriceSavings:
                for name, value in attrs:
                    if name == 'class':
                        if value == 'price-value':
                            self.inPrice = True
                        elif value == 'price-label':
                            self.inDiscount = True
            elif self.inPriceBox:
                for name, value in attrs:
                    if name == 'class':
                        if value == 'price-value':
                            self.inMSRP = True

    def handle_endtag(self, tag):
        if tag == 'li':
            if self.inLi:
                self.productHash[self.url] = {}
                self.productHash[self.url]["brand"] = "COACH"
                self.productHash[self.url]["product"] = self.product
                self.productHash[self.url]["image"] = self.image
                self.productHash[self.url]["price"] = self.price
                self.productHash[self.url]["msrp"] = self.msrp
                self.productHash[self.url]["discount"] = self.discount
                self.productHash[self.url]["soldout"] = self.soldout
                if self.smallImages > 0:
                    self.productHash[self.url]["smallImage"] = self.smallImages
                self.smallImages = []
                self.soldout = 0
                self.inLi = False
        elif tag == 'div':
            if self.inPriceSavings:
                self.inPriceSavings = False
            elif self.inPriceBox:
                self.inPriceBox = False
            elif self.inItemText:
                self.inItemText = False
            elif self.inGridContainer:
                self.inGridContainer = False
        elif tag == 'p':
            if self.inPriceSavings:
                self.inPriceSavings = False
            elif self.inPriceBox:
                self.inPriceBox = False
        elif tag == 'span':
            if self.inMSRP:
                self.inMSRP = False
            elif self.inPrice:
                self.inPrice = False
            elif self.inDiscount:
                self.inDiscount = False

    def handle_data(self, data):
        if self.inMSRP:
            self.msrp = data.strip().replace("$","").replace(",","")
             #print "DEBUG: msrp=%s" % self.msrp
        elif self.inPrice:
            self.price = data.strip().replace("$","").replace(",","")
             #print "DEBUG: price=%s" % self.price
        elif self.inDiscount:
            self.discount = data.strip().replace("With ", "").replace(" discount","")
             #print "DEBUG: discount=%s" % self.discount

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
            
        parser = coachoutletParser()
        parser.dirname = dirname
        parser.feed(html)

        output = open(filename + ".json", "w")
        output.write(json.dumps(parser.productHash))
        output.close()
