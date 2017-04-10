# -*- coding: utf-8 -*-
import requests
import MySQLdb
import time

from com.market.main.Basic import Basic

orderId = 6255953960092311552
status = 0
while True:
    conn = MySQLdb.connect(host='192.168.60.59', port=5200, user='root', passwd='', db='lsh_oms', charset="utf8")
    cursor = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
    cursor.execute('select order_status from order_head where order_code = {0}'.format(orderId))
    data = cursor.fetchall()
    conn.close()
    for status in data:
        print status['order_status']
    if status['order_status'] == 22 :
        BasicApi = Basic()
        cookie = BasicApi.mis_login()
        host = BasicApi.mis_url()  # 获取host
        url = '/order/user/cancel'
        headers = {'Cookie':'MISSESSID=8hvc8gpn5fh5cserkqnnit7d54; zone_id=1001'}
        params = {'order_id':str(orderId),'remarks':''}
        #time.sleep(2)
        result = requests.post(host + url,headers=headers,params=params)
        print result.text
        break
    else :
        False