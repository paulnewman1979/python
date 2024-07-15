#!/usr/local/bin/python

import urllib
from html.parser import HTMLParser
import sys
import re
from html.entities import entitydefs

class bensParser(HTMLParser):
    inDealTitle = False
    inProdImage = False
    inProdUrl = False
    inDealBox = False

    url = ""
    title = ""
    promo_hash = {}

    def __init__(self, ben_url):
        self.promo_hash = {}
        HTMLParser.__init__(self)
    
        self.inDealTitle = False
        self.inProdImage = False
        self.inProdUrl = False
        self.inDealBox = False
        self.pattern = re.compile(" +")
        self.ben_url = ben_url

    def handle_starttag(self, tag, attrs):
        url=""

        if tag == "article":
            self.inDealBox = True
        elif tag == 'div':
            for name, value in attrs:
                if name == 'class':
                    if value == 'deabox__title__links':
                        self.inDealTitle = True
                        self.content = ""
        elif tag == 'img':
            for name, value in attrs:
                if name == "class" and value == "lazyload dealbox__sidebar1__image":
                    self.inProdImage = True
                elif name == "data-src" and self.inProdImage:
                    self.prodImage = value.replace("//", "http://")
        elif tag == "a":
            if self.inDealTitle:
                for name, value in attrs:
                    if name == "class" and value == "link clicktrack-submit":
                        self.inProdUrl = True
                    if name == 'href' and self.inProdUrl:
                        self.url = value
                        self.inProdUrl = False

    def handle_endtag(self, tag):
        if tag == 'div':
            if self.inDealTitle:
                self.inDealTitle = False
        elif tag == "article":
            title = self.title.strip().rstrip()
            self.promo_hash[title] = []
            self.promo_hash[title].append(self.ben_url)
            self.promo_hash[title].append(self.prodImage)
            self.title = ""
            self.prodImage = ""
            self.inProdImage = False
            self.inDealBox = False

    def handle_data(self, data):
        # print(f"inDealTitle={self.inDealTitle} data={data}")
        if self.inDealTitle:
            newData = re.sub(self.pattern, " ", data.strip().rstrip().replace('\r', ' '))
            if self.title == "":
                self.title = newData
            else:
                self.title += " " + newData

    def handle_entityref(self, name):
        if entitydefs.has_key(name):
            self.handle_data(entitydefs[name]) 
        else: 
            self.handle_data('&'+name+';') 

if __name__ == '__main__':

    if len(sys.argv) < 2:
        print("usage: ", sys.argv[0], " filename")
    else:
        filename = sys.argv[1]
        input = open(filename, "r")
        html = input.read()
        input.close()
            
        parser = bensParser()
        parser.feed(html)
        for title in parser.promo_hash:
            print(title, "\t", parser.promo_hash[title][0], "\t", parser.promo_hash[title][1])

