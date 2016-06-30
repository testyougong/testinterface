# -*- coding: UTF-8 -*-
import unittest

import requests
import xlrd

from com.market.main.Basic import Basic


class SkuGetlistTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_skugetlist(self):
        BasicApi = Basic()
        token = BasicApi.login()#获取登录token
        url = BasicApi.basic_url()#获取url

        excel = xlrd.open_workbook('/Users/zhouxin/PycharmProjects/testinterface/testcase.xlsx')
        sheet = excel.sheets()[0]
        nrows = sheet.nrows

        for i in range(1,nrows):#从第二行开始取
            cat = sheet.cell(i,0).value
            pn = sheet.cell(i,1).value
            rn = sheet.cell(i,2).value

            params = {'cat': cat, 'pn': int(pn), 'rn': int(rn),'token':token}
            result = requests.get(url + '/item/sku/getlist', params = params,timeout = 0.9)

            assert result.status_code == 200
            if (result.json()['ret'] != ""):
                self.assertEqual(0, result.json()['ret'])
                assert result.json()['content']['item_list'] != ''
                cat = bytes(cat)
                print "接口 /item/sku/getlist?cat="+cat+"------------OK！"

            else:
                cat = bytes(cat)
                print "接口 /item/sku/getlist?cat="+cat+"------------Failure！"
                self.assertEqual(0, result.json()['ret'])


if __name__ == "__main__":
    unittest.main()
