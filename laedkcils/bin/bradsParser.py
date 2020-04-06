#!/usr/bin/python

import urllib
from html.parser import HTMLParser
import sys
from html.entities import entitydefs

class bradsParser(HTMLParser):
    inDealBox = False
    inProdImage = False
    inPostText = False
    inDealContent = False
    ACount = 0
    inStrong = False

    url = ''
    title = ''
    promo_hash = {}

    def __init__(self):
        self.promo_hash = {}
        HTMLParser.__init__(self)
    
        self.inDealBox = False
        self.inProdImage = False
        self.inPostText = False
        self.inDealContent = False
        self.ACount = 0
        self.inStrong = False
        self.inTitle = False

    def handle_starttag(self, tag, attrs):
        url=''

        if tag == 'div':
            for name, value in attrs:
                if name == 'class':
                    if value == 'row':
                        self.inDealBox = True
                    elif value == 'col large-5 medium-5 product small-12':
                        self.inProdImage = True
                    elif value == 'col information large-7 medium-7 small-12':
                        self.inDealContent = True
                        self.content = ''
                    elif value == 'advertiser-disclosure-link' or value == 'flag':
                        self.inPostText = True
        elif tag == 'img':
            if self.inProdImage:
                for name, value in attrs:
                    if name == 'style' and value == 'display: none':
                        break;
                    elif name == 'src':
                        self.prodImage = value
                        #print('DEBUG: image=%s' % self.prodImage)
        elif tag == 'a':
            if self.inDealBox and self.inDealContent:
                for name, value in attrs:
                    if name == 'class' and value != 'go-link':
                        break;
                    elif name == 'href':
                        self.url = value
        elif tag == 'h3':
            if self.inDealContent:
                self.inTitle = True

    def handle_endtag(self, tag):
        if tag == 'div':
            if self.inPostText:
                self.inPostText = False
            elif self.inProdImage:
                self.inProdImage = False
            elif self.inDealContent:
                self.inDealContent = False
            elif self.inDealBox:
                self.promo_hash[self.title] = []
                self.promo_hash[self.title].append(self.url)
                self.promo_hash[self.title].append(self.prodImage)
                self.title = ''
                self.inDealBox = False

    def handle_data(self, data):
        if self.inTitle:
            #print("DEBUG: title = %s" % data)
            self.title += data
            self.inTitle = False

    def handle_entityref(self, name):
        if entitydefs.has_key(name):
            self.handle_data(entitydefs[name]) 
        else: 
            self.handle_data('&'+name+';') 

if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf8')

    if len(sys.argv) < 2:
        print('usage: ', sys.argv[0], ' filename')
    else:
        filename = sys.argv[1]
        input = open(filename, 'r')
        html = input.read()
        input.close()
            
        parser = bradsParser()
        parser.feed(html)
        for title in parser.promo_hash:
            print('deal: %s\t%s\t%s' % (title, parser.promo_hash[title][0], parser.promo_hash[title][1]))

