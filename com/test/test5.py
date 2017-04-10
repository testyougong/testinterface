# -*- coding: UTF-8 -*-

import re
import MySQLdb

print(re.match('ww', 'www.runoob.com').span())  # 在起始位置匹配
print(re.match('com', 'www.runoob.com'))         # 不在起始位置匹配
print(re.search('com', 'www.runoob.com').span())
conn = MySQLdb.connect(host='192.168.60.59', port=5200, user='root', passwd='', db='lsh_market_dev', charset="utf8")
cursor = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
try:
    cursor.execute('insert into sku_blacklist(id,sku_id,status,uid,created_at,updated_at) values (20,100000,2,1,1,1)')
    conn.commit()
except:
    conn.rollback()
conn.close()


