# -*- coding: UTF-8 -*-
import unittest

import requests
import xlrd

from com.market.main.Basic import Basic
from com.market.main.MySQLdb import MySQLdb


class TestOrderCase3(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass


    def test_OrderInit(self):
        BasicApi = Basic()
        token = BasicApi.login()  # 获取登录token
        url = BasicApi.basic_url()  # 获取url

        # 操作excel
        excel = xlrd.open_workbook('/Users/zhouxin/PycharmProjects/testinterface/testcase.xls')
        sheet = excel.sheets()[2]
        nrows = sheet.nrows

        #order_excel = xlrd.open_workbook('/Users/zhouxin/PycharmProjects/testinterface/order.xls')
        #order_sheet = order_excel.sheets()[0]
        #order_nrows = order_sheet.nrows

        for i in range(1, nrows):  # 从第二行开始取
            sku_list = sheet.cell(i,0).value
            tab = sheet.cell(i,1).value
            use_coupon = sheet.cell(i,2).value
            pay_type = sheet.cell(i, 3).value
            code = sheet.cell(1, 4).value
            address_id = sheet.cell(i,5).value
            money = sheet.cell(i, 6).value

            #从order.xls中取prepare接口中生成的信息
            #code = order_sheet.cell(0,0).value
            #address_id = order_sheet.cell(0,1).value
            #money = order_sheet.cell(0,2).value

            #print code

            params = {'sku_list':str(sku_list),'tab':int(tab),'use_coupon':int(use_coupon),'code':str(code),'token':token,'address_id':str(address_id),'money':str(money),'pay_type':pay_type}
            result = requests.post(url+'/shopping/order/init',params = params)
            ResponseTime = (result.elapsed.microseconds) / 1000
            print "init接口响应时间:" + str(ResponseTime) + "ms"
            print result.text

            #从数据库取值验证是否入库
            #order_id = result.json()['content']['order_id']
            #print order_id
            #db = MySQLdb()
            #db_order_id = db.MySQL("'select order_id from order_head where order_id = '"+order_id+";")
            #print db_order_id
            #self.assertEqual(str(order_id), db_order_id.strip('\n'))

            assert result.status_code == 200
            if (result.json()['ret'] != ""):
                if(result.json()['ret'] == -10046 ):
                    self.assertEqual('系统有些繁忙, 休息一下,请您稍后再试'.decode('UTF-8'), result.json()['msg'])
                    print "接口 /shopping/order/init?sku_list="+str(sku_list)+"&tab="+str(tab)+"&use_coupon="+str(use_coupon)+"------------系统有些繁忙, 休息一下,请您稍后再试"
                elif (result.json()['ret'] == -10022):
                    self.assertEqual('商品仓储类型不一致'.decode('UTF-8'), result.json()['msg'])
                    print "接口 /shopping/order/init?sku_list="+str(sku_list)+"&tab="+str(tab)+"&use_coupon="+str(use_coupon)+"------------商品仓储类型不一致"
                elif (result.json()['ret'] == -10001):
                    self.assertEqual('稍等片刻，您的订单已提交, 请不要重复提交'.decode('UTF-8'), result.json()['msg'])
                    print "接口 /shopping/order/init?sku_list=" + str(sku_list) + "&tab=" + str(tab) + "&use_coupon=" + str(use_coupon) + "------------稍等片刻，您的订单已提交, 请不要重复提交"
                else:
                    self.assertEqual(0, result.json()['ret'])
                    print "接口 /shopping/order/init?sku_list="+str(sku_list)+"&tab="+str(tab)+"&use_coupon="+str(use_coupon)+"------------OK！"
            else:
                print "接口 /shopping/order/init------------Failure！"
                self.assertEqual(0, result.json()['ret'])


if __name__ == "__main__":
    unittest.main()
