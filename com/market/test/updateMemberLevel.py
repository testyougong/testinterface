# -*- coding: utf-8 -*-
import MySQLdb
import requests
import sys

from com.market.main.Basic import Basic
reload(sys)
sys.setdefaultencoding('utf-8')


BasicApi = Basic()
host = BasicApi.mis_url()  # 获取host
headers = {'Cookie':'MISSESSID=8hvc8gpn5fh5cserkqnnit7d54; zone_id=1000'}

conn = MySQLdb.Connect(host='192.168.60.59', port=5200, user='root', passwd='', db='lsh_market_dev', charset="utf8")
cursor = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
cursor.execute("select uid from user_member where member_level = 3 and zone_id = 1000 limit 300")
uid = cursor.fetchall()
for row in uid :
    print row['uid']
    uid = row['uid']
    member_level=2
    params = {'uid':uid,'member_level':member_level}
    result = requests.post( host +'/customermanage/user/updatemember',params = params,headers=headers)
    print result.text
