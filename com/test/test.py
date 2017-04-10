#!/usr/bin/python
#-*-coding:utf-8-*-
import threading
import time
import MySQLdb
import json
import requests
# select sku_id from item_sale where zone_id = 1000 limit 100;

conn = MySQLdb.connect(host='192.168.60.59', port=5200, user='root', passwd='', db='lsh_market_dev', charset="utf8")
cursor = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
sql = "select sku_id from item_sale where zone_id = 1000 limit 5"
cursor.execute(sql)
data = cursor.fetchall()
params = json.dumps(data)
url = "http://qa2.market-api.wmdev2.lsh123.com/goods/sku/getinfoforrisk?sku_ids="+params
response = requests.get(url)
#转化为字典形式
#for row in data:
    #print type(row)
    #print row

#返回元组
print data

#元组转列表
#print list(data)

#返回列表
print params

#将字典中长整形转换为整形或字符串
sku_id = data[0]
sku_id['sku_id'] = int(sku_id['sku_id'])
#sku_id['sku_id'] = str(sku_id['sku_id'])
print sku_id

#取出字典中的一个参数
sku_id = data[0]
print sku_id['sku_id']

#输出元组中每一个字段
for i in data:
    print i

#print json.dumps(response.json())
print '请求时间为:'+str(response.elapsed.total_seconds())+'s'