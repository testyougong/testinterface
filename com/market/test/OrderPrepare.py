# -*- coding: UTF-8 -*-
import unittest
import xlwt
import requests
import xlrd
import json

from xlutils.copy import copy
from com.market.main.Basic import Basic


class TestOrderCase2(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass


    def test_OrderPrepare(self):
        BasicApi = Basic()
        #token = BasicApi.login()  # 获取登录token
        token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1aWQiOiI4ODAzMDM3NDcxNDM2NjE2ODgxIiwiY3JlYXRlZF9hdCI6MTQ4MTQ2ODUxOX0.QmpBanIomBCLLczmlacKnduTVB3e2nLLkc3nTv4W-j8'
        url = BasicApi.basic_url()  # 获取url

        #操作excel
        excel = xlrd.open_workbook('/Users/zhouxin/PycharmProjects/testinterface/testcase.xls')
        sheet = excel.sheets()[2]
        nrows = sheet.nrows

        wb = copy(excel)
        for i in range(1, nrows):  # 从第二行开始取
            sku_list = sheet.cell(i,0).value
            tab = sheet.cell(i,1).value
            use_coupon = sheet.cell(i,2).value

            params = {'sku_list':str(sku_list),'tab':int(tab),'use_coupon':int(use_coupon),'token':token}
            result = requests.post(url+'/shopping/order/prepare',params = params)
            ResponseTime = (result.elapsed.microseconds) / 1000
            print "prepare接口响应时间:" + str(ResponseTime) + "ms"

            #从json中获取code,address_id,money字段
            code = result.json()['content']['code']
            order_list = result.json()['content']['order_list']
            head_info = order_list[0]['head_info']
            address_id = head_info['address_id']
            money = head_info['money']

            #print code

            #将code,address_id,money字段写入testcase.xls

            ws = wb.get_sheet(2)
            ws.write(i, 4, code)
            ws.write(i, 5, address_id)
            ws.write(i, 6, money)
            ws.write(i,7,json.dumps(result.json()))
            wb.save('/Users/zhouxin/PycharmProjects/testinterface/testcase.xls')


            #新建excel,将code,address_id,money写入order.xls
            #file = xlwt.Workbook()
            #table = file.add_sheet('order', cell_overwrite_ok=True)
            #table.write(0, 0, code)
            #table.write(0, 1, address_id)
            #table.write(0, 2, money)
            #file.save('/Users/zhouxin/PycharmProjects/testinterface/order.xls')

            assert result.status_code == 200
            if (result.json()['ret'] != ""):
                if(result.json()['ret'] == -10046 ):
                    self.assertEqual('系统有些繁忙, 休息一下,请您稍后再试'.decode('UTF-8'), result.json()['msg'])
                    print "接口 /shopping/order/prepare?sku_list="+str(sku_list)+"&tab="+str(tab)+"&use_coupon"+str(use_coupon)+"------------系统有些繁忙, 休息一下,请您稍后再试!"
                elif (result.json()['ret'] == -10022):
                    self.assertEqual('商品仓储类型不一致'.decode('UTF-8'), result.json()['msg'])
                    print "接口 /shopping/order/prepar?sku_listy="+str(sku_list)+"&tab="+str(tab)+"&use_coupon"+str(use_coupon)+"------------商品仓储类型不一致"
                else:
                    self.assertEqual(0, result.json()['ret'])
                    print "接口 /shopping/order/prepare?sku_list="+str(sku_list)+"&tab="+str(tab)+"&use_coupon"+str(use_coupon)+"------------OK！"
            else:
                print "接口 /shopping/order/prepare------------Failure！"
                self.assertEqual(0, result.json()['ret'])


if __name__ == "__main__":
    unittest.main()
