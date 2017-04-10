# -*- coding: utf-8 -*-
import os
import urllib2
import requests
import sys


for i in range(1, len(sys.argv)):
   print len(sys.argv)
   sequence = sys.argv[1]
   print sequence

request = urllib2.Request("http://www.baidu.com")
r = urllib2.urlopen(request)
print r.read()

b = requests.get("http://www.baidu.com")
print b.text