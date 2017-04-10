import MySQLdb
import json
import requests
# select sku_id from item_sale where zone_id = 1000 limit 100;

conn = MySQLdb.connect(host='192.168.60.59', port=5200, user='root', passwd='', db='lsh_market_dev', charset="utf8")
cursor = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
sql = "select sku_id from item_sale where zone_id = 1000 limit 5"
cursor.execute(sql)
data = cursor.fetchall()
print data
set = set()
for row in data:
    set.add(row['sku_id'])
print set
sku_ids = ""
for sku_id in set:
    sku_ids += str(sku_id)
    sku_ids += ","
print sku_ids[0:-1]

skus = ""
for row in data:
    skus += str(row['sku_id'])
    skus += ","
print skus[0:-1]
