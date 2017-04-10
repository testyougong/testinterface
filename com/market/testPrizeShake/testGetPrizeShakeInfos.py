# -*- coding: utf-8 -*-
import requests
import json

list=[]
for k in range(0,1000):
    try:
        host = 'http://qa.market-api.wmdev2.lsh123.com'
        result = requests.get(host + '/Operate/prize/getprizeshakeinfos?item_min=10&type=2&activity_id=619&item_max=100')
        #print json.dumps(result.json())
        ResponseTime = (result.elapsed.microseconds) / 1000
        print "shake接口响应时间:" + str(ResponseTime) + "ms"
        time = list.append(ResponseTime)

    except Exception, e:
        print Exception, ":", e
        print result.text
total = 0
for j in list:
    total+=j

avg = total/len(list)
print "shake接口平均响应时间:" + str(avg) +'ms'