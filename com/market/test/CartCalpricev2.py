# -*- coding: UTF-8 -*-
import unittest

import requests
import xlrd

from com.market.main.Basic import Basic


class TestOrderCase1(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass


    def test_CartCalpricev2(self):
        BasicApi = Basic()
        #token = BasicApi.login()  # 获取登录token
        token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1aWQiOiI4ODAzMDM3NDcxNDM2NjE2ODgxIiwiY3JlYXRlZF9hdCI6MTQ4MTQ2ODUxOX0.QmpBanIomBCLLczmlacKnduTVB3e2nLLkc3nTv4W-j8'
        url = BasicApi.basic_url()  # 获取url

        # 操作excel
        excel = xlrd.open_workbook('/Users/zhouxin/PycharmProjects/testinterface/testcase.xls')
        sheet = excel.sheets()[2]
        nrows = sheet.nrows

        for i in range(1, nrows):  # 从第二行开始取
            sku_list = sheet.cell(i,0).value
            tab = sheet.cell(i,1).value

            params = {'sku_list':str(sku_list),'tab':int(tab),'token':token}
            result = requests.post(url+'/shopping/cart/calpricev2',params = params)
            ResponseTime = (result.elapsed.microseconds) / 1000
            print "calpricev2接口响应时间:" + str(ResponseTime) + "ms"
            print result.text

            assert result.status_code == 200
            if (result.json()['ret'] != ""):
                if(result.json()['ret'] == -10046 ):
                    self.assertEqual('系统有些繁忙, 休息一下,请您稍后再试'.decode('UTF-8'), result.json()['msg'])
                    print "接口 /shopping/cart/calpricev2?sku_list="+str(sku_list)+"&tab="+str(tab)+"------------系统有些繁忙, 休息一下,请您稍后再试!"
                else:
                    #self.assertEqual(0, result.json()['ret'])
                    print "接口 /shopping/cart/calpricev2?sku_list="+str(sku_list)+"&tab="+str(tab)+"------------OK！"
            else:
                print "接口 /shopping/cart/calpricev2------------Failure！"
                self.assertEqual(0, result.json()['ret'])


if __name__ == "__main__":
    unittest.main()
