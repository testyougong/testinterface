# -*- coding: UTF-8 -*-
import MySQLdb
import requests
import json
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

wmSkuId = raw_input("请输入6位物美码:")
flag = True
while flag:
    depot = raw_input('请输入仓库号:')
    if depot.upper() == 'DC10' :
        supplierId = 1
        marketId = 1
        zoneId = 1000
        flag = False
    elif depot.upper() == 'DC31' :
        supplierId = 2
        marketId = 1
        zoneId = 1000
        flag = False
    elif depot.upper() == 'DC41' :
        supplierId = 7
        marketId = 1
        zoneId = 1000
        flag = False
    elif depot.upper() == 'DC42' :
        supplierId = 11
        marketId = 1
        zoneId = 1000
        flag = False
    elif depot.upper() == 'DC43' :
        supplierId = 12
        marketId = 1
        zoneId = 1000
        flag = False
    elif depot.upper() == 'DC09' :
        supplierId = 3
        marketId = 1
        zoneId = 1001
        flag = False
    elif depot.upper() == 'DC37' :
        supplierId = 4
        marketId = 1
        zoneId = 1001
        flag = False
    elif depot.upper() == 'DC55':
        supplierId = 5
        marketId = 3
        zoneId = 1002
        flag = False
    elif depot.upper() == 'DC59' :
        supplierId = 6
        marketId = 3
        zoneId = 1002
        flag = False
    elif depot.upper() == 'DC59-1' :
        supplierId = 10
        marketId = 3
        zoneId = 1002
        flag = False
    else :
        print 'DC不存在'
        flag = True

class createSku():
    def mis_url(self):
        mis_url = 'http://qa.market-mis.wmdev2.lsh123.com'
        return mis_url

    def mis_login(self):
        url = self.mis_url()
        user = {'email':'admin@lsh123.com','pwd':'111111qQ'}
        result = requests.post(url + '/account/user/checklogin',params=user)
        cookies = result.headers.get('Set-Cookie')
        return cookies

    def createWmSku(self):
        host = self.mis_url()  # 获取host
        conn = MySQLdb.connect(host='192.168.60.59', port=5200, user='root', passwd='', db='lsh_market_dev', charset="utf8")
        cursor = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        sql = 'select * from sap_sku where sku_id = {0} and market_id = {1}'.format(wmSkuId,marketId)
        cursor.execute(sql)
        #如果物美库中有此商品
        if cursor.rowcount == 1:
            code = str(wmSkuId).zfill(18)
            sql = 'select market_id from item_supply where code = {0} and market_id = {1}'.format(code,marketId)
            cursor.execute(sql)
            if cursor.rowcount == 1:
                print '已经从物美库中添加过此品'
            else :
                params = {'wm_sku_id': str(wmSkuId), 'market_id': marketId}
                headers = {'Cookie': self.mis_login()}
                result = requests.post(host + '/item/sku/addfromwm',headers = headers,params = params)
                if result.json()['ret'] == 0 :
                    print "从物美库添加商品成功"
                    item_name = result.json()['content']['item_name']
                    barcode = result.json()['content']['barcode']
                    item_id = result.json()['content']['item_id']
                    brand = result.json()['content']['brand']
                    properties = '[{"name":"taste","value":""},{"name":"sku_spec","value":"1 件"},{"name":"grade","value":""},{"name":"pack_style","value":""},{"name":"sale_unit","value":"个 "},{"name":"supply_pkg_unit","value":"个"},{"name":"supply_pkg_count","value":"1"},{"name":"shelf_life","value":"9999"},{"name":"store_temperature","value":"常温"},{"name":"vender_place","value":"__HWQT__"},{"name":"product_country","value":"CN"}]'
                    params = {'item_name': str(item_name), 'barcode': barcode ,'item_id': item_id,'brand': brand,'sku_define': 1,'category_id': "001002001",'img_list[]': 'e9afe3c82ad8547ad3a977','properties': properties}
                    result = requests.post(host + '/item/sku/update', headers=headers, params=params)
                    if result.json()['ret'] == 0 :
                        print '链商商品创建成功'
                    else :
                        print result.text
                else :
                    print '添加异常'
                    print result.text
        else :
            print '物美库中无此商品',
            return False
        conn.close()

    def createSkuPirce(self):
        conn = MySQLdb.connect(host='192.168.60.59', port=5200, user='root', passwd='', db='lsh_market_dev',charset="utf8")
        cursor = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        code = str(wmSkuId).zfill(18)
        sql = "select * from supply_info where code = {0} and market_id = {1} and depot = '{2}' and supplier_id = {3}".format(code,marketId,depot.upper(),supplierId)
        cursor.execute(sql)
        if cursor.rowcount == 1:
            print '货主信息表中已有该商品数据'
        else :
            sql = "insert into supply_info (market_id,supplier_id,code,supply_price,status,created_at,updated_at,depot) values ("+bytes(marketId)+","+bytes(supplierId)+",'"+code+"','10.00','1','1477469480','1477469480','"+depot.upper()+"')"
            try :
                cursor.execute(sql)
                conn.commit()
                if cursor.rowcount == 1 :
                    print '货主信息表插入数据成功'
            except:
                # Rollback in case there is any error
                conn.rollback()
                print '货主信息表插入数据时出现错误，并已回滚'
        sql = "select * from wm_supply_price where code = {0} and market_id = {1} and depot = '{2}' and supplier_id = {3}".format(code,marketId,depot.upper(),supplierId)
        cursor.execute(sql)
        if cursor.rowcount == 1:
            print '物美供货价表中已有该商品数据'
        else:
            sql = "insert into wm_supply_price (market_id,supplier_id,code,supply_price,created_at,updated_at,depot) values ("+bytes(marketId)+","+bytes(supplierId)+",'"+code+"','10.00','1477469480','1477469480','"+depot.upper()+"')"
            try:
                cursor.execute(sql)
                conn.commit()
                if cursor.rowcount == 1 :
                    print '物美供货价表插入数据成功'
            except:
                # Rollback in case there is any error
                conn.rollback()
                print '物美供货价表插入数据时出现错误，并已回滚'
        conn.close()

    def createMarketSku(self):
        host = self.mis_url()  # 获取host
        conn = MySQLdb.connect(host='192.168.60.59', port=5200, user='root', passwd='', db='lsh_market_dev',charset="utf8")
        cursor = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        sql = 'select name from sap_sku where sku_id = {0} and market_id = {1}'.format(wmSkuId,marketId)
        cursor.execute(sql)
        data = cursor.fetchall()
        for row in data:
            name = row['name']
            #print name
        code = str(wmSkuId).zfill(18)
        sql = 'select item_id from item_supply where code = {0} and market_id = {1}'.format(code,marketId)
        cursor.execute(sql)
        data = cursor.fetchall()
        for row in data:
            itemId = row['item_id']
            #print itemId
        params = {'name':str(name),'item_id':str(itemId),'sale_unit':10,'sale_unit_name':'个','sale_price':100,'moq':1,'order_limit':1000,'day_limit':10000,'max_inventory_num':"",'status':3,'limit_type':1,'limit_detail':[]}
        headers = {'Cookie': self.mis_login()}
        result = requests.post(host + '/item/sale/update', headers=headers, params=params)
        if result.json()['ret'] == 0 :
            print '销售商品创建成功'
        else :
            data = {
                    "is_new":1,
                    "type":1
            }
            data['zone_code'] = zoneId
            data['item_id'] = itemId
            if depot.upper() == 'DC10':
                data['rule_code'] = 1
            elif depot.upper() == 'DC31':
                data['rule_code'] = 2
            elif depot.upper() == 'DC41':
                data['rule_code'] = 4
            elif depot.upper() == 'DC42':
                data['rule_code'] = 9
            elif depot.upper() == 'DC43':
                data['rule_code'] = 10
            elif depot.upper() == 'DC09':
                data['rule_code'] = 1
            elif depot.upper() == 'DC37':
                data['rule_code'] = 2
            elif depot.upper() == 'DC41':
                data['rule_code'] = 4
            elif depot.upper() == 'DC55':
                data['rule_code'] = 1
            elif depot.upper() == 'DC59':
                data['rule_code'] = 2
            elif depot.upper() == 'DC59-1':
                data['rule_code'] = 8
            else :
                print '仓库不存在,无法创建出货规则'
            #print data
            headers = {'Content-Type': 'application/json', 'api-version': 'v1.0', 'random': '12345', 'platform': 'web'}
            result = requests.post('http://atp.lsh123.com/api/atp/java/v1/mis/updateSaleRule', data = json.dumps(data), headers = headers)
            if result.json()['status'] == 0 :
                print '出货规则创建成功'
            else :
                print result.text
            params = {'name': str(name), 'item_id': str(itemId), 'sale_unit': 10, 'sale_unit_name': '个','sale_price': 100, 'moq': 1, 'order_limit': 1000, 'day_limit': 10000, 'max_inventory_num': "",'status': 3, 'limit_type': 1, 'limit_detail': []}
            if(zoneId == 1000):
                headers = {'Cookie': self.mis_login()+';zone_id=1000'}
            elif (zoneId == 1001):
                headers = {'Cookie': self.mis_login()+';zone_id=1001'}
            elif (zoneId == 1002):
                headers = {'Cookie': self.mis_login()+';zone_id=1002'}
            result = requests.post(host + '/item/sale/update', headers=headers, params=params)
            if result.json()['ret'] == 0:
                print '销售商品创建成功'
            else :
                print result.text
        conn.close()

if __name__ ==  '__main__':
    create = createSku()
    cws = create.createWmSku()
    if cws == False :
        print '终止建品'
    else :
        create.createSkuPirce()
        create.createMarketSku()