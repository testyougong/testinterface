# -*- coding: utf-8 -*-
import requests
import MySQLdb

host = 'http://qa.market-mis.wmdev2.lsh123.com'
headers = {'Cookie':'MISSESSID=8hvc8gpn5fh5cserkqnnit7d54; zone_id=1002'}

conn = MySQLdb.Connect(host='192.168.60.59', port=5200, user='root', passwd='', db='lsh_market_dev', charset="utf8")
cursor = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
cursor.execute("select A.uid , B.address_id from user_info as A left join user_address as B on A.uid = B.uid where A.zone_id = 1002 and B.status = 3 and B.is_default = 1")
data = cursor.fetchall()
for row in data :
    uid = row['uid']
    addressId = row['address_id']
    zone_id = 1002
    skuList = '[{"sku_id":"120639","qty":"1","selected":"1"}]'
    params = {'uid':uid,'sku_list':skuList,'address_id':addressId,'coupon_id':'','invoice_type':2,'zone_id':zone_id}
    try:
        result = requests.post( host +'/order/ka/init',params = params,headers=headers)
        print result.text
    except Exception,e:
        print e
    conn = MySQLdb.Connect(host='192.168.60.59', port=5200, user='root', passwd='', db='lsh_oms', charset="utf8")
    cursor = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
    cursor.execute("select order_code , order_status from order_head where user_code = {0} order by order_time desc limit 1".format(uid))
    data = cursor.fetchall()
    for row in data:
        orderId = row['order_code']
        status = row['order_status']
        if status == 12:
            params = {'order_id': orderId}
            try:
                result = requests.post(host + '/order/user/approve', params=params, headers=headers)
                print result.text
            except Exception, e:
                print e