# -*- coding: utf-8 -*-
import requests
import MySQLdb

marketUrl = 'http://qa.market.wmdev2.lsh123.com'
misUrl = 'http://qa.market-mis.wmdev2.lsh123.com'
zoneId = raw_input("请输入地域id:")
flag = True
while flag :
    if zoneId == '1000':
        users = ["13466640320", "16001346603", "16001346606", "16001346609", "16001346612", "16001346617"]
        cookieZoneId = ';zone_id=1000'
        skuList = '[{"qty":5,"sku_id":"104285"},{"qty":1,"sku_id":"120748"}]'
        flag = False
    elif zoneId == '2000':
        users = ['15726624809']
        cookieZoneId = ';zone_id=2000'
        skuList = '[{"qty":1,"sku_id":"120943"}]'
        flag = False
    elif zoneId == '1001':
        users = ['16001346601']
        cookieZoneId = ';zone_id=1001'
        skuList = '[{"qty":1,"sku_id":"120898"}]'
        flag = False
    elif zoneId == '1002':
        users = ['16001346604']
        cookieZoneId = ';zone_id=1002'
        skuList = '[{"qty":5,"sku_id":"120639"}]'
        flag = False
    else :
        print '输入的地域id不存在'
        flag = True

class UserOrder():
    def misLogin(self):
        user = {'email': 'admin@lsh123.com', 'pwd': '111111qQ'}
        result = requests.post(misUrl + '/account/user/checklogin', params = user)
        cookies = result.headers.get('Set-Cookie')
        return cookies

    def marketLogin(self,username):
        headers = {'device-id': 'market'}
        user = {'username': username, 'password': '000000'}
        result = requests.post(marketUrl + '/user/info/login', params = user, headers = headers)
        if result.json()['ret'] == 1004 :
            result = requests.post(marketUrl + '/captcha/sms/sendVerifyUnusual?cellphone=' + username)
            #print result.text
            headers = {'Cookie': self.misLogin() + cookieZoneId}
            result = requests.get(misUrl + '/customermanage/user/searchverify?cellphone=' + username,headers = headers)
            resultContent = result.json()['content'][0]
            verifyCode = resultContent['verify_code']
            user = {'username': username, 'password': '000000', 'verify_code': verifyCode}
            result = requests.post(marketUrl + '/user/info/login', params = user, headers=headers)
        token = result.json()['content']['token']
        #print token
        return token

    def marketOrder(self):
        for i in range(0,len(users)):
            cellphone = users[i]
            token = self.marketLogin(cellphone)
            params = {'sku_list': skuList, 'tab': 1, 'use_coupon': 0, 'use_cash_coupon':0, 'pay_type':1,'token': token}
            try:
                result = requests.post(marketUrl + '/shopping/order/prepare', params = params)
            except Exception, e:
                print Exception,":",e
            #print result.text
            code = result.json()['content']['code']
            moneyInfo = result.json()['content']['money_info']
            money = moneyInfo['money']
            orderInfo = result.json()['content']['order_info']
            addressId = orderInfo['address_id']
            params = {'sku_list': skuList, 'tab': 1, 'code': code,'token': token, 'address_id': addressId, 'money': money, 'pay_type': 1}
            try:
                result = requests.post(marketUrl + '/shopping/order/init', params = params)
            except Exception, e:
                print Exception,":",e
            print result.text

    def misApprove(self):
        for i in range(0,len(users)):
            cellphone = users[i]
            conn = MySQLdb.Connect(host='192.168.60.59', port=5200, user='root', passwd='', db='lsh_market_dev',charset="utf8")
            cursor = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
            cursor.execute("select uid from user_info where cellphone = {0}".format(cellphone))
            data = cursor.fetchall()
            for row in data :
                uid = row['uid']
                conn = MySQLdb.Connect(host='192.168.60.59', port=5200, user='root', passwd='', db='lsh_oms', charset="utf8")
                cursor = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
                cursor.execute("select order_code , order_status from order_head where user_code = {0} order by order_time desc limit 1".format(uid))
                data = cursor.fetchall()
                for row in data:
                    orderId = row['order_code']
                    status = row['order_status']
                    if status == 12:
                        params = {'order_id': orderId}
                        headers = {'Cookie': self.misLogin() + cookieZoneId}
                        try:
                            result = requests.post(misUrl + '/order/user/approve', params = params, headers = headers)
                            if result.json()['ret'] != 0 :
                                print result.text
                        except Exception, e:
                            print Exception, ":", e

if __name__ == '__main__' :
    userOrder = UserOrder()
    userOrder.marketOrder()#商城批量下单
    userOrder.misApprove()#mis批量审核订单
