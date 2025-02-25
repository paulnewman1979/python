#!/usr/bin/python3

import sys
import os
import json
from urllib import request
import urllib3
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
from bensParser import bensParser
from moonParser import moonParser
from walletParser import walletParser

price_match1 = re.compile("\$[0-9]+ off \$[0-9]+")
price_match2 = re.compile("[0-9]+%")
price_match3 = re.compile("\$[0-9.]+")
price_match4 = re.compile("[0-9]+\$")
price_match5 = re.compile("[0-9]+ off [0-9]+")

def print_usage(cmd):
    print(f"usage: {cmd} [options]")
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
        items = line.split("\t")
        if len(items) == 1:
            old_title_hash[items[0]] = "https://bensbargains.com/"
        else:
            old_title_hash[items[0]] = items[1]
        line = input.readline()
    input.close()


def record_new_title(new_title_hash):
    new_title = open("../tmp/new.title.txt", "w")
    for title in new_title_hash.keys():
        url = new_title_hash[title]
        line = f"{title}\t{url}\n"
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

def record_info_used_count(ignore_used_info_count):
    with open("../tmp/ignore.used.info.count.json", "w+") as fp:
        json.dump(ignore_used_info_count, fp, indent=4)

def load_info_used_count():
    try:
        with open("../tmp/ignore.used.info.count.json") as fp:
            return json.load(fp)
    except Exception:
        return None

def record_new_deal(new_deal_hash):
    new_deal = open("../result/new.deal.txt", "w")
    for title in new_deal_hash:
        prices = getPrices(title)
        url = new_deal_hash[title][0]
        for price in prices:
            new_deal.write(price)
            new_deal.write("\t")
        new_deal.write("\n")
        line = f"{title}\n\t{url}"
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
    imageParser.feed(html.decode("latin1"))
    return imageParser.images

def fetch_new_title_slick(old_title_hash, new_deal_hash, new_title_hash, filtered_deal_hash, selector):
    print("fetch_new_title_slick")
    hasNewTitle = True
    index = 1
    cur = datetime.now()
    timestamp = int(((cur.year * 100 + cur.month) * 100 + cur.day) * 100 + cur.hour)
    dirname = f"../data/slickdeal/{timestamp}"
    try:
        os.mkdir(dirname)
    except:
        pass

    while hasNewTitle and index <= 30:
        print("\tprocessing ", index)
        url = f"/forums/filtered/?f=9&page={index}&order=desc&sort=lastpost&icid=filtered_user"
        conn = http.client.HTTPSConnection("slickdeals.net",timeout=100)

        conn.request("GET", url)
        response = conn.getresponse()
        if response.status != 200:
            print(response.status)
        html=response.read()
        filename = f"../data/slickdeal/{timestamp}/{index}.html"
        output = open(filename, "wb")
        output.write(html)
        output.close()

        parser = sdParser()
        parser.feed(html.decode("latin1"))
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
    timestamp = int(((cur.year * 100 + cur.month) * 100 + cur.day) * 100 + cur.hour)
    dirname = f"../data/dealwiki/{timestamp}"
    try:
        os.mkdir(dirname)
    except:
        pass

    while hasNewTitle and index <= 3:
        print("\tprocessing ", index)
        url = f"/?p={index}"
        conn = http.client.HTTPSConnection("dealwiki.net")
        conn.request("GET", url)
        response = conn.getresponse()
        if response.status != 200:
            print(response.status, respones.reason)
        html=response.read()
        filename = f"../data/dealwiki/{timestamp}/{index}.html"
        output = open(filename, "wb")
        output.write(html)
        output.close()

        parser = dealwikiParser()
        parser.feed(html.decode("latin1"))
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



def fetch_new_title_brads(old_title_hash, new_deal_hash, new_title_hash, filtered_deal_hash, selector):
    imageParser = sdImageParser()
    print("fetch_new_title_brads")
    hasNewTitle = True
    index = 1
    cur = datetime.now()
    timestamp = int(((cur.year * 100 + cur.month) * 100 + cur.day) * 100 + cur.hour)
    dirname = f"../data/bradsdeal/{timestamp}"
    try:
        os.mkdir(dirname)
    except:
        pass

    while hasNewTitle and index <= 30:
        print("\tprocessing ", index)
        url = f"deals?page={index}"
        conn = http.client.HTTPSConnection("www.bradsdeals.com")
        conn.request("GET", url)
        response = conn.getresponse()
        if response.status != 200:
            print(response.status)
        html=response.read()
        filename = f"../data/bradsdeal/{timestamp}/{index}.html"
        output = open(filename, "wb")
        output.write(html)
        output.close()

        parser = bradsParser()
        parser.feed(html.decode("latin1"))
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

def fetch_new_title_sea(old_title_hash, new_deal_hash, new_title_hash, filtered_deal_hash, selector):
    print("fetch_new_title_sea")
    hasNewTitle = True
    index = 1
    cur = datetime.now()
    timestamp = int(((cur.year * 100 + cur.month) * 100 + cur.day) * 100 + cur.hour)
    dirname = f"../data/dealsea/{timestamp}"
    try:
        os.mkdir(dirname)
    except:
        pass

    while hasNewTitle and index <= 30:
        print("\tprocessing ", index)
        url = f"https://dealsea.com/?page={index}"
        if index == 1:
            url = "https://dealsea.com/"
        http_client = urllib3.PoolManager()
        headers = {
            "User-Agent": "curl/8.1.2",
            "Accept": "*/*"
        }
        resp = http_client.request("GET", url, headers=headers)
        html = resp.data
        if resp.status != 200:
            return
        filename = f"../data/dealsea/{timestamp}/{index}.html"
        output = open(filename, "wb")
        output.write(html)
        output.close()

        parser = seaParser()
        parser.feed(html.decode("latin1"))
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
    timestamp = int(((cur.year * 100 + cur.month) * 100 + cur.day) * 100 + cur.hour)
    dirname = f"../data/wallet/{timestamp}"
    try:
        os.mkdir(dirname)
    except:
        pass

    while hasNewTitle and index <= 7:
        print("\tprocessing ", index)
        url = f"http://www.fatwallet.com/?liststyle=grid&page={index}"
        html = request.urlopen(url).read()
        filename = f"../data/wallet/{timestamp}/{index}.html"
        output = open(filename, "wb")
        output.write(html)
        output.close()

        parser = walletParser()
        parser.feed(html.decode("latin1"))
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
    timestamp = int(((cur.year * 100 + cur.month) * 100 + cur.day) * 100 + cur.hour)
    dirname = f"../data/dealmoon/{timestamp}"
    try:
        os.mkdir(dirname)
    except:
        pass

    while hasNewTitle and index <= 30:
        print("\tprocessing ", index)
        url = f"http://www.dealmoon.com/{index}"
        if index == 1:
            url = "http://www.dealmoon.com/"
        html = request.urlopen(url).read()
        filename = f"../data/dealmoon/{timestamp}/{index}.html"
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

def fetch_new_title_bens_bargains(old_title_hash, new_deal_hash, new_title_hash, filtered_deal_hash, selector):
    print("fetch_new_title_bens_bargains")
    hasNewTitle = True
    index = 1
    cur = datetime.now()
    timestamp = int(((cur.year * 100 + cur.month) * 100 + cur.day) * 100 + cur.hour)
    dirname = f"../data/bens/{timestamp}"
    try:
        os.mkdir(dirname)
    except:
        pass

    headers = {
        # ":authority": "bensbargains.com",
        # ":method": "GET",
        # ":path": "/4/"
        # ":scheme": "https",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9",
        "Cookie": "u_here=b1c7f58ebcc74010e0c07c690060ce5f; BIGipServerbensbargains-web_POOL=1402081290.0.0000; usprivacy=1YYY; _gid=GA1.2.1750296392.1696270638; _ga=GA1.1.1261740853.1696218133; homepageFilters=%7B%22categories%22%3Anull%2C%22merchants%22%3Anull%2C%22brands%22%3Anull%2C%22prices%22%3A%5B0%2C7%5D%2C%22priceRanges%22%3Anull%2C%22expired%22%3A1%2C%22sort%22%3A6%2C%22sortName%22%3A%22Hottest%22%7D; cf_clearance=5WPxiEhABD9646D1LhqNe2KzRz0RsWM4x0KXIyq5qWw-1696272444-0-1-611bf024.61efb7d0.361aafc4-0.2.1696272444; OptanonConsent=isGpcEnabled=0&datestamp=Mon+Oct+02+2023+11%3A48%3A15+GMT-0700+(Pacific+Daylight+Time)&version=202305.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=ef9559d3-2658-491b-846b-22a8c1e6689c&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CSPD_BG%3A0%2CC0004%3A0%2CC0005%3A0%2CC0003%3A0&AwaitingReconsent=false; _ga_RX4CCXCQLY=GS1.1.1696270645.3.1.1696272500.0.0.0",
        "Dnt": "1",
        # "Referer": "://bensbargains.com/3/"
        "Sec-Ch-Ua": "Google Chrome\";v=\"117\", \"Not;A=Brand\";v=\"8\", \"Chromium\";v=\"117\"",
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": "macOS",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
    }


    while hasNewTitle and index <= 30:
        print("\tprocessing ", index)
        url = f"https://bensbargains.com/{index}/"
        if index == 1:
            url = "https://bensbargains.com/hot/"
        http_client = urllib3.PoolManager()
        resp = http_client.request("GET", url, headers=headers)
        html = resp.data
        if resp.status != 200:
            return
        filename = f"../data/bens/{timestamp}/{index}.html"
        output = open(filename, "wb")
        output.write(html)
        output.close()

        parser = bensParser(url)
        parser.feed(html.decode("latin1"))
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
                    filtered_deal_hash[title] = selector.filterRule
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
            fullname = f"{curdir}/{filename}"
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

if __name__ == "__main__":
    run_type = "web"
    run_dir = ""
    try:
        opts, args = getopt.getopt(sys.argv[1:], "t:d:")
    except:
        print_usage(sys.argv[0])
        sys.exit(1)
    for opt, arg in opts:
        if opt == "-t":
            run_type = arg
        elif opt == "-d":
            run_dir = arg

    if run_type != "web" and run_type != "local":
        print_usage(sys.argv[0])
        sys.exit(2)
        
    # reload(sys)
    # sys.setdefaultencoding("latin1")

    old_title_hash = {}
    new_deal_hash = {}
    new_title_hash = {}
    filtered_deal_hash = {}
    selector = dealSelector(load_info_used_count())

    if run_type == "web":
        load_old_title(old_title_hash)
        fetch_new_title_bens_bargains(old_title_hash, new_deal_hash, new_title_hash, filtered_deal_hash, selector)
        fetch_new_title_brads(old_title_hash, new_deal_hash, new_title_hash, filtered_deal_hash, selector)
        fetch_new_title_slick(old_title_hash, new_deal_hash, new_title_hash, filtered_deal_hash, selector)
        fetch_new_title_sea(old_title_hash, new_deal_hash, new_title_hash, filtered_deal_hash, selector)
        # fetch_new_title_dealwiki(old_title_hash, new_deal_hash, new_title_hash, filtered_deal_hash)
        # fetch_new_title_wallet(old_title_hash, new_deal_hash, new_title_hash, filtered_deal_hash)
        # fetch_new_title_moon(old_title_hash, new_deal_hash, new_title_hash, filtered_deal_hash)
    else:
        load_old_title(old_title_hash)
        train_old_title(old_title_hash, new_deal_hash, filtered_deal_hash)
        # train_old_web(run_dir, new_deal_hash, new_title_hash, filtered_deal_hash)

    # reload(sys)
    # sys.setdefaultencoding("utf8")

    record_new_deal(new_deal_hash)
    compose_html(new_deal_hash)
    record_new_title(new_title_hash)
    record_filtered_deal(filtered_deal_hash)
    record_info_used_count(selector.ignoredInfoUsedCount)
