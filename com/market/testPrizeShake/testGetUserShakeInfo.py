# -*- coding: utf-8 -*-
import requests
import json
import xlrd

list=[]
excel = xlrd.open_workbook('/Users/zhouxin/PycharmProjects/testinterface/query_result2.xls',encoding_override="utf-8")
sheet = excel.sheets()[0]
nrows = sheet.nrows
for k in range(1,4):
    for i in range(1, nrows):
        try:
            host = 'http://qa.market-api.wmdev2.lsh123.com'
            excel_uid = sheet.cell(i, 0).value
            uid = excel_uid.replace(',', '')
            print uid
            activity_id = 620
            params = {'uid': str(uid), 'activity_id': activity_id}
            host = 'http://qa.market-api.wmdev2.lsh123.com'
            result = requests.get(host + '/Operate/prize/getusershakeInfo?',params = params)
            print json.dumps(result.json())
            ResponseTime = (result.elapsed.microseconds) / 1000
            print "shake接口响应时间:" + str(ResponseTime) + "ms"
            time = list.append(ResponseTime)
        except Exception,e:
            print Exception, ":", e
            print result.text

total = 0
for j in list:
    total+=j

avg = total/len(list)
print "shake接口平均响应时间:" + str(avg) +'ms'