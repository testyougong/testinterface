#coding=utf-8
import redis
import MySQLdb

flag = True
sku_id = raw_input("请输入链商商品码:")
number = int(raw_input('请输入需要修改的库存量:'))
while (flag):
    DC = str(raw_input("请输入DC:"))
    if DC.upper() =='DC10':
        string = 'atp:inventoryLogic:1000:{0}'.format(sku_id,number)
        key = "1:DC10"
        flag = False
    elif DC.upper() == 'DC31':
        string = 'atp:inventoryLogic:1000:{0}'.format(sku_id,number)
        key ="2:DC31"
        flag = False
    elif DC.upper() =='DC42':
        string = 'atp:inventoryLogic:1000:{0}'.format(sku_id,number)
        key = "1:DC42"
        flag = False
    elif DC.upper() == 'DC43':
        string = 'atp:inventoryLogic:1000:{0}'.format(sku_id,number)
        key ="2:DC43"
        flag = False
    elif DC.upper() == 'DC41':
        string = 'atp:inventoryLogic:1000:{0}'.format(sku_id,number)
        key ="3:DC41"
        flag = False
    elif DC.upper() =='DC09':
        string = 'atp:inventoryLogic:1001:{0}'.format(sku_id,number)
        key = "1:DC09"
        flag = False
    elif DC.upper()=='DC37':
        string = 'atp:inventoryLogic:1001:{0}'.format(sku_id,number)
        key ="2:DC37"
        flag = False
    elif DC.upper()=='DC40':
        string = 'atp:inventoryLogic:1001:{0}'.format(sku_id,number)
        key ="2:DC40"
        flag = False
    elif DC.upper() == 'DC55':
        string = 'atp:inventoryLogic:1002:{0}'.format(sku_id,number)
        key = "1:DC55"
        flag = False
    elif DC.upper() =='DC59':
        string = 'atp:inventoryLogic:1002:{0}'.format(sku_id,number)
        key = "2:DC59"
        flag = False
    else:
        print "DC不存在，请重新输入DC"
        flag = True

try:
    r= redis.StrictRedis(host='192.168.60.59',port=6379)
    r.hset(string, key,number)
    print "redis中商品"+sku_id+'的数量为:'+r.hget(string, key)
except Exception:
    print 'redis连接失败'

sql = "update INVENTORY_LOGIC set INVENTORY_QUANTITY = {0} where SKU_ID = {1} and DC = '{2}'".format(number,sku_id,DC)
# print sql
item = MySQLdb.connect(host='192.168.60.48', port=5201, user='root', passwd='root123', db='lsh-atp1', charset="utf8")
itemCursor = item.cursor(cursorclass=MySQLdb.cursors.DictCursor)
itemCursor.execute(sql)
item.commit()

sql2 = "select INVENTORY_QUANTITY as result  from INVENTORY_LOGIC where SKU_ID = '{0}' and DC='{1}';".format(sku_id,DC)
itemCursor.execute(sql2)

result = itemCursor.fetchall()[0]['result']
print "数据库中商品"+sku_id+'的数量为:'+str(result)
item.close()
