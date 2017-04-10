# -*- coding: UTF-8 -*-
import unittest

import requests
import xlrd
import json
import MySQLdb

from xlutils.copy import copy
from com.market.main.Basic import Basic
#from com.market.main.MySQLdb import MySQLdb


class OrderTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_order(self):
        BasicApi = Basic()
        #token = BasicApi.login()  # 获取登录token
        token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1aWQiOiIzMTA4MjM1ODY5NzQwMDYzMDM0IiwiY3JlYXRlZF9hdCI6MTQ4MTYyODEzMn0.EhYZYsReULBc_WDn7IW9CMCVTFZlGjMQEk-6ehlstKM'
        url = BasicApi.basic_url()  # 获取url

        #CartCalpricev2
        # 操作excel
        excel = xlrd.open_workbook('/Users/zhouxin/PycharmProjects/testinterface/testcase.xls')
        sheet = excel.sheets()[3]
        nrows = sheet.nrows

        for i in range(1, nrows):  # 从第二行开始取
            sku_list = sheet.cell(i,0).value
            tab = sheet.cell(i,1).value

            params = {'sku_list':str(sku_list),'tab':int(tab),'token':token}
            result = requests.post(url+'/shopping/cart/calpricev2',params = params)
            ResponseTime = (result.elapsed.microseconds) / 1000
            print "calpricev2接口响应时间:" + str(ResponseTime) + "ms"

            assert result.status_code == 200
            if (result.json()['ret'] == 0):
                print "接口 /shopping/cart/calpricev2?sku_list="+str(sku_list)+"&tab="+str(tab)+"------------Pass!"
            else:
                print "接口 /shopping/cart/calpricev2------------Failure！"
                print json.dumps(result.json())
                self.assertEqual(0, result.json()['ret'])

        #OrderPrepare
        wb = copy(excel)
        for i in range(1, nrows):  # 从第二行开始取
            sku_list = sheet.cell(i, 0).value
            tab = sheet.cell(i, 1).value
            use_coupon = sheet.cell(i, 2).value

            params = {'sku_list': str(sku_list), 'tab': int(tab), 'use_coupon': int(use_coupon), 'token': token}
            result = requests.post(url + '/shopping/order/prepare', params=params)
            ResponseTime = (result.elapsed.microseconds) / 1000
            print "prepare接口响应时间:" + str(ResponseTime) + "ms"

            # 从json中获取code,address_id,money字段
            code = result.json()['content']['code']
            order_list = result.json()['content']['order_list']
            head_info = order_list[0]['head_info']
            address_id = head_info['address_id']
            money = head_info['money']

            # print code

            # 将code,address_id,money字段写入testcase.xls
            ws = wb.get_sheet(3)
            ws.write(i, 4, code)
            ws.write(i, 5, address_id)
            ws.write(i, 6, money)
            wb.save('/Users/zhouxin/PycharmProjects/testinterface/testcase.xls')

            # 新建excel,将code,address_id,money写入order.xls
            # file = xlwt.Workbook()
            # table = file.add_sheet('order', cell_overwrite_ok=True)
            # table.write(0, 0, code)
            # table.write(0, 1, address_id)
            # table.write(0, 2, money)
            # file.save('/Users/zhouxin/PycharmProjects/testinterface/order.xls')

            assert result.status_code == 200
            if (result.json()['ret'] == 0):
                print "接口 /shopping/order/prepare?sku_list=" + str(sku_list) + "&tab=" + str(
                        tab) + "&use_coupon" + str(use_coupon) + "------------Pass!"
            else:
                print "接口 /shopping/order/prepare------------Failure！"
                print json.dumps(result.json())
                self.assertEqual(0, result.json()['ret'])

        #OrderInit
        for i in range(1, nrows):  # 从第二行开始取
            sku_list = sheet.cell(i, 0).value
            tab = sheet.cell(i, 1).value
            use_coupon = sheet.cell(i, 2).value
            pay_type = sheet.cell(i, 3).value
            #code = sheet.cell(1, 4).value
            #address_id = sheet.cell(i, 5).value
            #money = sheet.cell(i, 6).value

            params = {'sku_list': str(sku_list), 'tab': int(tab), 'use_coupon': int(use_coupon), 'code': str(code),
                      'token': token, 'address_id': str(address_id), 'money': str(money), 'pay_type': pay_type}
            result = requests.post(url + '/shopping/order/init', params=params)
            ResponseTime = (result.elapsed.microseconds) / 1000
            print "init接口响应时间:" + str(ResponseTime) + "ms"
            #print json.dumps(result.json())
            ws = wb.get_sheet(3)
            ws.write(i, 7, json.dumps(result.json()))
            wb.save('/Users/zhouxin/PycharmProjects/testinterface/testcase.xls')

            """
            # 从数据库取值验证是否入库
            order_id = result.json()['content']['order_id']
            #print order_id
            db = MySQLdb()
            db_order_code = db.MySQL_OMS("'select order_code from order_head where order_code = '"+order_id+";")
            #print db_order_code
            self.assertEqual(str(order_id), db_order_code.strip('\n'))
            """

            # 从数据库取值验证是否入库
            order_id = result.json()['content']['order_id']
            conn = MySQLdb.connect(host='192.168.60.48', port=5201, user='root', passwd='root123', db='lsh_oms', charset="utf8")
            cursor = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
            sql = "select order_code from order_head where order_code = '{0}'".format(order_id)
            cursor.execute(sql)
            data = cursor.fetchall()
            order_code = data[0]
            actual_order_code = str(int(order_code['order_code']))
            self.assertEqual(order_id,actual_order_code)

            assert result.status_code == 200
            if (result.json()['ret'] == 0):
                print "接口 /shopping/order/init?sku_list=" + str(sku_list) + "&tab=" + str(
                    tab) + "&use_coupon=" + str(use_coupon) + "------------Pass！"
            else:
                print "接口 /shopping/order/init------------Failure！"
                print json.dumps(result.json())
                self.assertEqual(0, result.json()['ret'])



if __name__ == "__main__":
    unittest.main()
