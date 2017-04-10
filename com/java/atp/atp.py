#coding=utf-8

import MySQLdb
import redis
import time

#库存同步测试脚本
flag = True
while flag ==True:
    item_id = raw_input("请输入链商码:")
    DC = raw_input("请输入DC:")
    if DC.upper() == 'DC42' or DC.upper()=='DC43':
        zone_code = 1000
        market_id =1
        flag = False
    elif DC.upper() =='DC09' or DC.upper() == 'DC37':
        zone_code = 1001
        market_id = 1
        flag = False
    elif DC.upper() =='DC55' or DC.upper() =='DC59':
        zone_code = 1002
        market_id =3 
        flag = False
    else:
        print "输入的DC错误，请重新输入"
print "地域id:"+str(zone_code)

#商品码转物美码
item = MySQLdb.connect(host='192.168.60.59', port=5200, user='root', passwd='', db='lsh_market_dev', charset="utf8")
itemCursor = item.cursor(cursorclass=MySQLdb.cursors.DictCursor)
itemCursor.execute("select code from item_supply where market_id = "+str(market_id)+" and item_id = "+str(item_id)+';')
code = itemCursor.fetchall()[0]['code']

#物美的库存数量,现在取Kafka中库存,不从物美表取了
"""
WuAtp = MySQLdb.connect(host='192.168.60.59', port=5200, user='root', passwd='', db='lsh_base', charset="utf8")
WuAtpCursor = WuAtp.cursor(cursorclass=MySQLdb.cursors.DictCursor)
WuAtpCursor.execute("select lbkum from item_delivery where werks = "+"'"+str(DC)+"'"+" and sku_id = "+str(code)+';')
try:
    lbkum = WuAtpCursor.fetchall()[0]['lbkum']
    print "物美库存量:"+ str(lbkum)
except Exception,e:
    print Exception,":",e
"""

#订单需扣减的库存数量
set = set()
   
oms = MySQLdb.connect(host='192.168.60.59', port=5200, user='root', passwd='', db='lsh_oms', charset="utf8")
omsCursor = oms.cursor(cursorclass=MySQLdb.cursors.DictCursor)
omsCursor.execute("SELECT order_code  FROM order_head  WHERE order_status IN (12, 20, 21)  AND region_code = "+str(zone_code)+";")
for row in omsCursor.fetchall() :
    #print row["order_id"]
    set.add(row["order_code"])
'''  
ofc = MySQLdb.connect(host='192.168.60.59', port=5200, user='root', passwd='',db='lsh_ofc', charset="utf8")
ofcCursor = ofc.cursor(cursorclass=MySQLdb.cursors.DictCursor)
if (DC == 'DC10' or DC == 'DC09'):
    sql = 'select order_id from ofc_bill where bill_type="ORDER" and system ="WUMART_SAP" and created_at >'+str(1491537988)+';'
    ofcCursor.execute(sql)
elif(DC == 'DC31' or DC == 'DC37'):
    sql = 'select order_id from ofc_bill where bill_type="ORDER" and system ="WUMART_SAP_JISHOU" and created_at >' + str(1491537988) + ';'
    ofcCursor.execute(sql)
for row in ofcCursor.fetchall() :
    #print row["order_id"]
    set.add(row["order_id"])
'''
       
orderIds = ""
for orderId in set:
    orderIds += str(orderId)
    orderIds += ","
orderIds = orderIds[0:-1]
           
atp = MySQLdb.connect(host='192.168.60.48', port=5201, user='root', passwd='root123', db='lsh-atp1', charset="utf8")
atpCursor = atp.cursor(cursorclass=MySQLdb.cursors.DictCursor)
atpCursor.execute("select ifnull(sum(HOLD_QTY),0) as HOLD_QTY from SKU_HOLD_QTY WHERE HOLD_ID IN (SELECT ID FROM SKU_HOLD WHERE status = 2 and SEQUENCE_ID IN ("+ orderIds + ")) and DC = "+"'"+str(DC.upper())+"'"+" and sku_id = "+str(item_id)+";")
order_atp = atpCursor.fetchall()[0]['HOLD_QTY']
print "订单待扣减量"+str(order_atp)


#商品预留数量
#SELECT ifnull(max(s.sale_unit), 0) FROM item_sale s INNER JOIN item_level l ON s.sku_id = l.sku_id WHERE s. STATUS = 2 AND s.item_id = 100096 AND s.zone_id = 1000 AND l. LEVEL IN (1, 2) ;
itematp = MySQLdb.connect(host='192.168.60.59', port=5200, user='root', passwd='', db='lsh_market_dev', charset="utf8")
itematpCursor = itematp.cursor(cursorclass=MySQLdb.cursors.DictCursor)
sql = "SELECT ifnull(max(s.sale_unit), 0) FROM item_sale s INNER JOIN item_level l ON s.sku_id = l.sku_id WHERE s. STATUS = 2 AND s.item_id = "+str(item_id)+" AND s.zone_id = "+str(zone_code)+" AND l. LEVEL IN (1,2);"
# print sql
itematpCursor.execute(sql)
item_atp = itematpCursor.fetchall()[0]['ifnull(max(s.sale_unit), 0)']
print "预留数量为:"+str(item_atp)

#链商库存
atpCursor.execute("select INVENTORY_QUANTITY from INVENTORY_LOGIC where SKU_ID = "+str(item_id) +" and DC= "+"'"+str(DC)+"'"+";")
atp = atpCursor.fetchall()[0]['INVENTORY_QUANTITY']
print "链商库存:"+str(atp)

#redis中库存
r= redis.StrictRedis(host='192.168.60.59',port=6379)
key = 'atp:inventoryLogic:'+str(zone_code)+':'+str(item_id)
if(DC.upper() == 'DC42'):
    field = '1:DC42'
elif(DC.upper() == 'DC43'):
    field = '2:DC43'
elif(DC.upper() == 'DC09'):
    field = '1:DC09'
elif(DC.upper() == 'DC37'):
    field = '2:DC37'
elif(DC.upper() == 'DC55'):
    field = '1:DC55'
elif(DC.upper() == 'DC59'):
    field = '2:DC59'
else:
    print "DC不存在"
print 'redis中库存为:'+r.hget(key,field)

#计算方式 物美库存-订单待扣减量-预留数量

