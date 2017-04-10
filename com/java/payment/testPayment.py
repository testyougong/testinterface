# -*- coding: utf-8 -*-
import json

import requests
import unittest
import time

from com.java.base.runTest import runTest
from xlutils.copy import copy
from com.java.base.db import db



class payment(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testPayment(self):
        # 操作excel
        testCase = runTest()
        excel = testCase.runPaymentTest("paymentcase.xls")
        sheet = excel.sheets()[0]
        nrows = sheet.nrows
        wb = copy(excel)
        ws = wb.get_sheet(0)
        amount = 0

        for i in range(1,2):
            host = 'http://testpay.wmdev2.lsh123.com'
            url = sheet.cell(i,4).value
            headers = {'Content-Type': 'application/json','api-version':'v1.0','random':'12345','platform':'web'}
            data = sheet.cell(i,5).value
            if sheet.cell(i,6).value != "" :
                sql =  json.loads(sheet.cell(i,6).value)['trade_id']
                tms = db()
                tradeId = tms.tmsQuery(sql)
                for row in tradeId :
                    row['receipt_order_id']
                data = json.loads(data)
                data['trade_id'] = row['receipt_order_id']
                ws.write(i,5,json.dumps(data))
                try:
                    result = requests.post(host + url, headers = headers, data = json.dumps(data))
                    print json.dumps(result.text)
                except Exception, e:
                    print Exception, ":", e
            else :
                try:
                    result = requests.post(host + url , headers = headers ,data = data)
                    print json.dumps(result.text)
                except Exception,e:
                    print Exception,":",e
            responseTime = (result.elapsed.microseconds) / 1000
            ws.write(i, 13, responseTime)
            ret = sheet.cell(i, 11).value
            if result.json()['ret'] == ret :
                print "第%d条用例pass" % i
                ws.write(i, 12, 'pass')
                amount += 1
            else:
                print "第%d条用例failure" % i
                ws.write(i, 12, result.json()['ret'])
                ws.write(i, 10, result.text)
            resultTime = time.strftime('%Y-%m-%d_%H:%M:%S')

        a = amount / float(1)
        ws.write(i, 15, "%.2f" % a)
        print "case通过率为%.2f" % a
        wb.save('/Users/zhouxin/PycharmProjects/testinterface/paymentTestCase/paymentTestResult_' + resultTime + '.xls')

if __name__ ==  '__main__':
    unittest.main()
