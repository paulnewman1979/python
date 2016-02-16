#!/usr/bin/python

import json
import urllib
import HTMLParser
import sys
import re
import os
from htmlentitydefs import entitydefs

class michaelkorsParser(HTMLParser.HTMLParser):
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
        if tag == 'div':
            for name, value in attrs:
                if name == 'class':
                    if value == 'product_panel':
                        self.inProductPanel = True
                    elif value == 'prod_name prod_name_width':
                        self.inProductName = True
                    elif value == 'product_description':
                        self.inProductDesp = True
        elif tag == 'a':
            if self.inProductPanel:
                for name, value in attrs:
                    if name == 'href':
                        self.url = value.replace("&amp;", "&")
        elif tag == 'img':
            if self.inProductPanel:
                for name, value in attrs:
                    if name == 'src':
                        self.image = value
        elif tag == 'span':
            if self.inProductDesp:
                for name, value in attrs:
                    if name == 'class' and value == 'was_price':
                        self.inMSRP = True
                    elif name == 'class' and value == 'now_price':
                        self.inPrice = True
        elif tag == 'h6':
            if self.inProductName:
                self.inH6 = True

    def handle_endtag(self, tag):
        if tag == 'div':
            if self.inProductName:
                self.inProductName = False
            elif self.inProductPanel:
                self.inProductPanel = False
            elif self.inProductDesp:
                self.inProductDesp = False
        elif tag == 'span':
            self.inPrice = False
            self.inMSRP = False
        elif tag == 'h6':
            self.inH6 = False

    def handle_data(self, data):
        if self.inPrice:
            self.price = data
        elif self.inMSRP:
            self.msrp = data
        elif self.inH6:
            self.product = data

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
            
        parser = michaelkorsParser()
        parser.dirname = dirname
        parser.feed(html)

        output = open(filename + ".json", "w")
        output.write(json.dumps(parser.productHash))
        output.close()
