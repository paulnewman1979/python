#!/usr/bin/python

import json
import urllib
import HTMLParser
import sys
import re
from htmlentitydefs import entitydefs

class sixpmParser(HTMLParser.HTMLParser):
    inBrandName = False
    inProductName = False
    inPrice = False
    inDiscount = False
    inStrong = False

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

    priceMatcher = re.compile('\$[0-9\.,]*')

    def __init__(self):
        HTMLParser.HTMLParser.__init__(self)
        self.inBrandName = False
        self.inProductName = False
        self.inPrice = False
        self.inDiscount = False
        self.inStrong = False
        self.productHash = {}
        priceMatcher = re.compile('\$[0-9\.,]*')

    def handle_price(self, price):
         #print "DEBUG: before price = %s" % price
        prices = self.priceMatcher.findall(price)
        clean_price = prices[0].replace(",", "")
        return clean_price
    
    def handle_starttag(self, tag, attrs):
        url=""

        if tag == 'span':
            for name, value in attrs:
                if name == 'class' and value == 'brandName':
                    self.inBrandName = True
                elif name == 'class' and value == 'productName':
                    self.inProductName = True
                elif name == 'class' and value == 'price-6pm':
                    self.inPrice = True
                elif name == 'class' and value == 'discount':
                    self.inDiscount = True
        elif tag == 'strong':
            if self.inDiscount:
                self.inStrong = True
        elif tag == 'a':
            for name, value in attrs:
                if name == 'href':
                    self.tmpUrl = value
                elif name == 'data-style-id':
                    self.url = "http://www.6pm.com%s" % self.tmpUrl
                     #print "DEBUG: url = %s" % self.url
        elif tag == 'img':
            for name, value in attrs:
                if name == 'src':
                    self.tmpImage = value
                elif name == 'class' and value == 'productImg':
                    self.image = self.tmpImage
                     #print "DEBUG: image = %s" % self.image

    def handle_endtag(self, tag):
        if tag == 'strong':
            self.inStrong = False
        elif tag == 'span':
            self.inBrandName = False
            self.inProductName = False
            self.inPrice = False
            if self.inDiscount:
                self.msrp = self.handle_price(self.msrp)
                 #print "DEBUG: msrp = %s" % self.msrp
                self.productHash[self.url] = {}
                self.productHash[self.url]["brand"] = self.brand
                self.productHash[self.url]["product"] = self.product
                self.productHash[self.url]["image"] = self.image
                self.productHash[self.url]["price"] = self.price
                self.productHash[self.url]["msrp"] = self.msrp
                self.productHash[self.url]["discount"] = self.discount
                self.msrp = ""
                self.inDiscount = False
            
    def handle_data(self, data):
        if self.inStrong:
            self.discount = data
             #print "DEBUG: discount = %s" % self.discount
        elif self.inPrice:
            self.price = self.handle_price(data)
             #print "DEBUG: price = %s" % self.price
        elif self.inBrandName:
            self.brand = data
             #print "DEBUG: brand = %s" % self.brand
        elif self.inProductName:
            self.product = data
             #print "DEBUG: product = %s" % self.product
        elif self.inDiscount:
            self.msrp = self.msrp + data

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
            
        parser = sixpmParser()
        parser.feed(html)

        for url in parser.productHash:
            brand = parser.productHash[url]["brand"]
            product = parser.productHash[url]["product"]
            image = parser.productHash[url]["image"]
            price = parser.productHash[url]["price"]
            msrp = parser.productHash[url]["msrp"]
            discount = parser.productHash[url]["discount"]
            print "%s,%s,%s,%s,%s,%s,%s" % (url, brand, product, image, price, msrp, discount)
