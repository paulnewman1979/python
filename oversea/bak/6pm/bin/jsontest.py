#!/usr/bin/python

import json
import sys

if __name__ == '__main__':
    productHash = {}
    productHash["product1"] = {}
    productHash["product1"]["price"] = 1
    productHash["product1"]["image"] = "image1"
    productHash["product2"] = {}
    productHash["product2"]["price"] = 2
    productHash["product2"]["image"] = "image2"
    print "%s" % json.dumps(productHash)

