#!/usr/bin/python

import urllib
import HTMLParser
import sys
from htmlentitydefs import entitydefs

class walletParser(HTMLParser.HTMLParser):
    inDealBox = False
    inProdImage = False
    inPostText = False
    inDealContent = False
    ACount = 0
    inStrong = False
    inPrice = False
    inNowPrice = False
    inWasPrice = False
    inCashback = False
    price = ""
    oldPrice = ""

    url = ""
    title = ""
    promo_hash = {}

    def __init__(self):
        self.promo_hash = {}
        HTMLParser.HTMLParser.__init__(self)
    
        self.inOffer = False
        self.inTop = False
        self.inImage = False
        self.inPrice = False
        self.inNowPrice = False
        self.inWasPrice = False
        self.inCashback = False
        self.price = ""
        self.oldPrice = ""

    def handle_starttag(self, tag, attrs):
        url=""

        if tag == 'a':
            for name, value in attrs:
                if name == 'href':
                    self.url = value
        elif tag == 'div':
            for name, value in attrs:
                if name == 'class':
                    if value == 'offer-cell':
                        self.inOffer = True
                    elif value == 'top':
                        if self.inOffer:
                            self.inTop = True
                    elif value == 'offer-image':
                        if self.inOffer:
                            self.inImage = True
                    elif value == 'offer-list-cashback':
                        if self.inOffer:
                            self.inCashback = True
                    elif value == 'offer-price':
                        if self.inOffer:
                            self.inPrice = True
        elif tag == 'img':
            if self.inTop:
                for name, value in attrs:
                    if name == 'data-original':
                        self.storeImage = value
            elif self.inImage:
                for name, value in attrs:
                    if name == 'data-original':
                        self.productImage = value
                    elif name == 'alt':
                        self.title = value
                        self.promo_hash[self.title] = []
                        self.promo_hash[self.title].append("http://www.fatwallet.com/" + self.url)
                        self.promo_hash[self.title].append("")
                        self.promo_hash[self.title].append("")
                        self.promo_hash[self.title].append("http:" + self.storeImage)
                        self.promo_hash[self.title].append("http:" + self.productImage)
        elif tag == 'span':
            if self.inPrice:
                for name, value in attrs:
                    if name == 'class':
                        if value == 'price':
                            self.inNowPrice = True
                        elif value == 'was-price':
                            self.inWasPrice = True
                            

    def handle_endtag(self, tag):
        if tag == 'div':
            if self.inOffer:
                if self.inTop:
                    if self.inCashback:
                        self.inCashback = False
                    else:
                        self.inTop = False
                elif self.inImage:
                    self.inImage = False
                elif self.inPrice:
                    self.inPrice = False
                    self.promo_hash[self.title][1] = self.price
                    self.promo_hash[self.title][2] = self.oldPrice
                    self.price = ""
                    self.oldPrice = ""
                else:
                    self.inOffer = False 
        elif tag == 'span':
            if self.inNowPrice:
                self.inNowPrice = False
            elif self.inWasPrice:
                self.inWasPrice = False

    def handle_data(self, data):
        data = data.strip()
        data = data.rstrip()
        if self.inNowPrice:
            self.price += data
        elif self.inWasPrice:
            self.oldPrice += data

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
            
        parser = walletParser()
        parser.feed(html)
        for title in parser.promo_hash:
            print "%s\t%s\t%s\t%s" % (title, parser.promo_hash[title][0], parser.promo_hash[title][1], parser.promo_hash[title][2])

