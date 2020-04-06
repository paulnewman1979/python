#!/usr/local/bin/python

import sys
import os
from urllib import request
import http.client
import getopt
import re
from datetime import datetime
from sdParser import sdParser
from bradsParser import bradsParser
from sdImageParser import sdImageParser
from dealwikiParser import dealwikiParser
from dealSelector import dealSelector
from seaParser import seaParser
from moonParser import moonParser
from walletParser import walletParser

price_match1 = re.compile('\$[0-9]+ off \$[0-9]+')
price_match2 = re.compile('[0-9]+%')
price_match3 = re.compile('\$[0-9.]+')
price_match4 = re.compile('[0-9]+\$')
price_match5 = re.compile('[0-9]+ off [0-9]+')

def print_usage(cmd):
    print("usage: %s [options]", cmd)
    print("\t-t (local|web), web as default")
    print("\t-d dir for local, necessary for type \"local\"")

def getPrices(title):
    global price_match1
    global price_match2
    global price_match3
    global price_match4
    global price_match5
    prices = price_match1.findall(title)
    if len(prices) == 0:
        prices = price_match2.findall(title)
    if len(prices) == 0:
        prices = price_match3.findall(title)
    if len(prices) == 0:
        prices = price_match4.findall(title)
    if len(prices) == 0:
        prices = price_match5.findall(title)
    return prices

def load_old_title(old_title_hash):
    input = open("../data/old.title.txt", "r")
    line = input.readline()
    while line:
        line = line.strip()
        index = 0
        for item in line.split("\t"):
            if index == 0:
                title = item
                index = 1
            else:
                url = item
                old_title_hash[title] = url
        line = input.readline()
    input.close()


def record_new_title(new_title_hash):
    new_title = open("../tmp/new.title.txt", "w")
    for title in new_title_hash.keys():
        url = new_title_hash[title]
        line = "%s\t%s\n" % (title, url)
        new_title.write(line)
    new_title.close()


def record_filtered_deal(filtered_deal_hash):
    filtered_deal = open("../tmp/filtered.deal.txt", "w")
    for title in filtered_deal_hash:
        filtered_rule = filtered_deal_hash[title]
        #filtered_deal.write(title.encode("iso-8859-15", "replace"))
        filtered_deal.write(title);
        filtered_deal.write("\n\t")
        filtered_deal.write(filtered_rule)
        filtered_deal.write("\n")
    filtered_deal.close()


def record_new_deal(new_deal_hash):
    new_deal = open("../result/new.deal.txt", "w")
    for title in new_deal_hash:
        prices = getPrices(title)
        url = new_deal_hash[title][0]
        for price in prices:
            new_deal.write(price)
            new_deal.write("\t")
        new_deal.write("\n")
        line = "%s\n\t%s" % (title, url)
        i = 4
        while i < len(new_deal_hash[title]):
            line += "\n\t"
            line += new_deal_hash[title][i]
            i += 1
        line += "\n\n"
        new_deal.write(line)
    new_deal.close()

def fetch_slick_images_new(url, conn):
    imageParser = sdImageParser()
    conn.request("GET", url)
#    print("detail url %s" % url)
    response = conn.getresponse()
    html=response.read()
    imageParser.feed(html.decode('latin1'))
    return imageParser.images

def fetch_new_title_slick(old_title_hash, new_deal_hash, new_title_hash, filtered_deal_hash):
    imageParser = sdImageParser()
    print("fetch_new_title_slick")
    selector = dealSelector()
    hasNewTitle = True
    index = 1
    cur = datetime.now()
    timestamp = "%i" % ( ( ( cur.year * 100 + cur.month) * 100 + cur.day ) * 100 + cur.hour )
    dirname = "../data/slickdeal/%s" % timestamp
    try:
        os.mkdir(dirname)
    except:
        pass

    while hasNewTitle and index <= 30:
        print("\tprocessing ", index)
        url='//forums/forumdisplay.php?f=9&page={0}&order=desc&sort=lastpost'.format(index) 
        conn = http.client.HTTPSConnection("slickdeals.net")
        conn.request("GET", url)
        response = conn.getresponse()
        if response.status != 200:
            print(response.status, respones.reason)
        html=response.read()
        filename = "../data/slickdeal/%s/%i.html" % (timestamp, index)
        output = open(filename, "wb")
        output.write(html)
        output.close()

        parser = sdParser()
        parser.feed(html.decode('latin1'))
        hasNewTitle = False
        for title in parser.promo_hash:
            if title not in old_title_hash:
                old_title_hash[title] = url
                hasNewTitle = True
                url = parser.promo_hash[title][0]
                new_title_hash[title] = url
                if selector.checkDeal(title, False):
                    new_deal_hash[title] = []
                    real_url = "http://slickdeals.net" + url
                    new_deal_hash[title].append(real_url)
                    new_deal_hash[title].append("")
                    new_deal_hash[title].append("")
                    for image in fetch_slick_images_new(url, conn):
                        new_deal_hash[title].append(image)
                else:
                    filtered_deal_hash[title] = selector.filterRule
        index += 1

def fetch_new_title_dealwiki(old_title_hash, new_deal_hash, new_title_hash, filtered_deal_hash):
    imageParser = sdImageParser()
    print("fetch_new_title_dealwiki")
    selector = dealSelector()
    hasNewTitle = True
    index = 1
    cur = datetime.now()
    timestamp = "%i" % ( ( ( cur.year * 100 + cur.month) * 100 + cur.day ) * 100 + cur.hour )
    dirname = "../data/dealwiki/%s" % timestamp
    try:
        os.mkdir(dirname)
    except:
        pass

    while hasNewTitle and index <= 3:
        print("\tprocessing ", index)
        url='/?p={0}'.format(index) 
        conn = http.client.HTTPSConnection("dealwiki.net")
        conn.request("GET", url)
        response = conn.getresponse()
        if response.status != 200:
            print(response.status, respones.reason)
        html=response.read()
        filename = "../data/dealwiki/%s/%i.html" % (timestamp, index)
        output = open(filename, "wb")
        output.write(html)
        output.close()

        parser = dealwikiParser()
        parser.feed(html.decode('latin1'))
        hasNewTitle = False
        for title in parser.promo_hash:
            if title not in old_title_hash:
                old_title_hash[title] = url
                hasNewTitle = True
                url = parser.promo_hash[title][0]
                new_title_hash[title] = url
                if selector.checkDeal(title, False):
                    new_deal_hash[title] = []
                    new_deal_hash[title].append(url)
                    new_deal_hash[title].append("")
                    new_deal_hash[title].append("")
                    i = 1
                    while i < len(parser.promo_hash[title]):
                        new_deal_hash[title].append(parser.promo_hash[title][i])
                        i += 1
                else:
                    filtered_deal_hash[title] = selector.filterRule
        index += 1



def fetch_new_title_brads(old_title_hash, new_deal_hash, new_title_hash, filtered_deal_hash):
    imageParser = sdImageParser()
    print("fetch_new_title_brads")
    selector = dealSelector()
    hasNewTitle = True
    index = 1
    cur = datetime.now()
    timestamp = "%i" % ( ( ( cur.year * 100 + cur.month) * 100 + cur.day ) * 100 + cur.hour )
    dirname = "../data/bradsdeal/%s" % timestamp
    try:
        os.mkdir(dirname)
    except:
        pass

    while hasNewTitle and index <= 30:
        print("\tprocessing ", index)
        url='deals?page={0}'.format(index) 
        conn = http.client.HTTPSConnection("www.bradsdeals.com")
        conn.request("GET", url)
        response = conn.getresponse()
        if response.status != 200:
            print(response.status, respones.reason)
        html=response.read()
        filename = "../data/bradsdeal/%s/%i.html" % (timestamp, index)
        output = open(filename, "wb")
        output.write(html)
        output.close()

        parser = bradsParser()
        parser.feed(html.decode('latin1'))
        hasNewTitle = False
        for title in parser.promo_hash:
            if title not in old_title_hash:
                old_title_hash[title] = url
                hasNewTitle = True
                url = parser.promo_hash[title][0]
                new_title_hash[title] = url
                if selector.checkDeal(title, False):
                    new_deal_hash[title] = []
                    real_url = "http://bradsdeals.com" + url
                    new_deal_hash[title].append(real_url)
                    new_deal_hash[title].append("")
                    new_deal_hash[title].append("")
                    i = 1
                    while i < len(parser.promo_hash[title]):
                        new_deal_hash[title].append(parser.promo_hash[title][i])
                        i += 1
                else:
                    filtered_deal_hash[title] = selector.filterRule
        index += 1

def fetch_new_title_sea(old_title_hash, new_deal_hash, new_title_hash, filtered_deal_hash):
    print("fetch_new_title_sea")
    selector = dealSelector()
    hasNewTitle = True
    index = 1
    cur = datetime.now()
    timestamp = "%i" % ( ( ( cur.year * 100 + cur.month) * 100 + cur.day ) * 100 + cur.hour )
    dirname = "../data/dealsea/%s" % timestamp
    try:
        os.mkdir(dirname)
    except:
        pass

    while hasNewTitle and index <= 30:
        print("\tprocessing ", index)
        url = 'http://dealsea.com/?page=%i' % index
        if index == 1:
            url = 'http://dealsea.com/'
        html = request.urlopen(url).read()
        filename = "../data/dealsea/%s/%i.html" % (timestamp, index)
        output = open(filename, "wb")
        output.write(html)
        output.close()

        parser = seaParser()
        parser.feed(html.decode('latin1'))
        hasNewTitle = False
        for title in parser.promo_hash:
            if title not in old_title_hash:
                hasNewTitle = True
                url = parser.promo_hash[title][0]
                new_title_hash[title] = url
                old_title_hash[title] = url
                if selector.checkDeal(title, False):
                    new_deal_hash[title] = []
                    new_deal_hash[title].append("http://dealsea.com" + url)
                    new_deal_hash[title].append("")
                    new_deal_hash[title].append("")
                    i = 1
                    while i < len(parser.promo_hash[title]):
                        new_deal_hash[title].append(parser.promo_hash[title][i])
                        i += 1
                else:
                    filtered_deal_hash[title] = selector.filterRule
        index += 1

def fetch_new_title_wallet(old_title_hash, new_deal_hash, new_title_hash, filtered_deal_hash):
    print("fetch_new_title_wallet")
    selector = dealSelector()
    hasNewTitle = True
    index = 1
    cur = datetime.now()
    timestamp = "%i" % ( ( ( cur.year * 100 + cur.month) * 100 + cur.day ) * 100 + cur.hour )
    dirname = "../data/wallet/%s" % timestamp
    try:
        os.mkdir(dirname)
    except:
        pass

    while hasNewTitle and index <= 7:
        print("\tprocessing ", index)
        url = 'http://www.fatwallet.com/?liststyle=grid&page=%i' % index
        html = request.urlopen(url).read()
        filename = "../data/wallet/%s/%i.html" % (timestamp, index)
        output = open(filename, "wb")
        output.write(html)
        output.close()

        parser = walletParser()
        parser.feed(html.decode('latin1'))
        hasNewTitle = False
        for title in parser.promo_hash:
            if title not in old_title_hash:
                hasNewTitle = True
                url = parser.promo_hash[title][0]
                new_title_hash[title] = url
                old_title_hash[title] = url
                if selector.checkDeal(title, False):
                    new_deal_hash[title] = []
                    new_deal_hash[title].append(url)
                    new_deal_hash[title].append(parser.promo_hash[title][1])
                    new_deal_hash[title].append(parser.promo_hash[title][2])
#print "was_price: %s" % parser.promo_hash[title][2]
                    i = 3
                    while i < len(parser.promo_hash[title]):
                        new_deal_hash[title].append(parser.promo_hash[title][i])
                        i += 1
                else:
                    filtered_deal_hash[title] = selector.filter_rule
        index += 1

def fetch_new_title_moon(old_title_hash, new_deal_hash, new_title_hash, filtered_deal_hash):
    print("fetch_new_title_moon")
    selector = dealSelector()
    hasNewTitle = True
    index = 1
    cur = datetime.now()
    timestamp = "%i" % ( ( ( cur.year * 100 + cur.month) * 100 + cur.day ) * 100 + cur.hour )
    dirname = "../data/dealmoon/%s" % timestamp
    try:
        os.mkdir(dirname)
    except:
        pass

    while hasNewTitle and index <= 30:
        print("\tprocessing ", index)
        url = 'http://www.dealmoon.com/%i' % index
        if index == 1:
            url = 'http://www.dealmoon.com/'
        html = request.urlopen(url).read()
        filename = "../data/dealmoon/%s/%i.html" % (timestamp, index)
        output = open(filename, "wb")
        output.write(html)
        output.close()

        parser = moonParser()
        parser.feed(html)
        hasNewTitle = False
        for title in parser.promo_hash:
            if title not in old_title_hash:
                hasNewTitle = True
                url = parser.promo_hash[title][0]
                new_title_hash[title] = url
                old_title_hash[title] = url
                if selector.checkDeal(title, False):
                    new_deal_hash[title] = []
                    new_deal_hash[title].append(url)
                    new_deal_hash[title].append("")
                    new_deal_hash[title].append("")
                    i = 1
                    while i < len(parser.promo_hash[title]):
                        new_deal_hash[title].append(parser.promo_hash[title][i])
                        i += 1
                else:
                    filtered_deal_hash[title] = selector.filter_rule
        index += 1

def train_old_title(old_title_hash, new_deal_hash, filtered_deal_hash):
    selector = dealSelector()
    for title in old_title_hash:
         if selector.checkDeal(title, False):
             url = old_title_hash[title]
             new_deal_hash[title] = []
             new_deal_hash[title].append(url)
         else:
             filtered_deal_hash[title] = selector.filter_rule

def train_old_web(run_dir, new_deal_hash, new_title_hash, filtered_deal_hash):
    selector = dealSelector()
    for curdir, dirnames, filenames in os.walk(run_dir):
        for filename in filenames:
            fullname = "%s/%s" % (curdir, filename)
            print("processing ", fullname)
            input = open(fullname, "r")
            html = input.read()
            input.close()

            parser = sdParser()
            parser.feed(html)
            for title in parser.promo_hash:
                if selector.checkDeal(title, False):
                    url = parser.promo_hash[title]
                    new_deal_hash[title] = url
                else:
                    filtered_deal_hash[title] = selector.filter_rule
        for dirname in dirnames:
            train_old_web(dirname, new_deal_hash, new_title_hash, filtered_deal_hash)

def compose_html(new_deal_hash):
    new_deal = open("../result/new.deal.html", "w")
    new_deal.write("<!DOCTYPE html><html><head><link rel=\"stylesheet\" type=\"text/css\" href=\"./deal.css\"></head>");
    new_deal.write("<body><table id=\"table-design\"><thead><th>Price</th><th>Title</th><th>Image</th></thead>")
    new_deal.write("<tbody>\n")
    for title in new_deal_hash:
        new_deal.write("<tr>")

        cur_price = ""
        was_price = ""
        prices = getPrices(title)
        url = new_deal_hash[title][0]
        for price in prices:
            cur_price += price + "&nbsp"
        new_deal.write("<td>\n")
        if new_deal_hash[title][1] != "":
            cur_price = new_deal_hash[title][1]
        new_deal.write(cur_price);

        was_price = new_deal_hash[title][2]
        if was_price != "":
            new_deal.write("&nbsp;<del>")
            new_deal.write(was_price)
            new_deal.write("</del>")
        new_deal.write("</td>\n")

        new_deal.write("<td>\n")
        new_deal.write("<a href=\"")
        new_deal.write(url)
        new_deal.write("\">")
        new_deal.write(title)
        new_deal.write("</a>")

        new_deal.write("<td>\n")
        new_deal.write("<a href=\"")
        new_deal.write(url)
        new_deal.write("\">")
        i = 3
        while i < len(new_deal_hash[title]) and i <= 7:
            new_deal.write("<img src=\"")
            new_deal.write(new_deal_hash[title][i])
            new_deal.write("\"/>\n")
            i += 1
        new_deal.write("</a>")
        new_deal.write("</td>\n")

        new_deal.write("</tr>")
    new_deal.write("</tbody>\n")
    new_deal.write("</table></body></html>\n")

if __name__ == '__main__':
    run_type = 'web'
    run_dir = ''
    try:
        opts, args = getopt.getopt(sys.argv[1:], "t:d:")
    except:
        print_usage(sys.argv[0])
        sys.exit(1)
    for opt, arg in opts:
        if opt == '-t':
            run_type = arg
        elif opt == '-d':
            run_dir = arg

    if run_type != "web" and run_type != "local":
        print_usage(sys.argv[0])
        sys.exit(2)
        
    #reload(sys)
    #sys.setdefaultencoding('latin1')

    old_title_hash = {}
    new_deal_hash = {}
    new_title_hash = {}
    filtered_deal_hash = {}

    if run_type == 'web':
        load_old_title(old_title_hash)
        fetch_new_title_slick(old_title_hash, new_deal_hash, new_title_hash, filtered_deal_hash)
        fetch_new_title_sea(old_title_hash, new_deal_hash, new_title_hash, filtered_deal_hash)
        fetch_new_title_brads(old_title_hash, new_deal_hash, new_title_hash, filtered_deal_hash)
        fetch_new_title_dealwiki(old_title_hash, new_deal_hash, new_title_hash, filtered_deal_hash)
#        fetch_new_title_wallet(old_title_hash, new_deal_hash, new_title_hash, filtered_deal_hash)
#       fetch_new_title_moon(old_title_hash, new_deal_hash, new_title_hash, filtered_deal_hash)
    else:
        load_old_title(old_title_hash)
        train_old_title(old_title_hash, new_deal_hash, filtered_deal_hash)
        #train_old_web(run_dir, new_deal_hash, new_title_hash, filtered_deal_hash)

    #reload(sys)
    #sys.setdefaultencoding('utf8')

    record_new_deal(new_deal_hash)
    compose_html(new_deal_hash)
    record_new_title(new_title_hash)
    record_filtered_deal(filtered_deal_hash)
