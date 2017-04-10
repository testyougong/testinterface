# -*- coding: utf-8 -*-
import os,sys
import logging
import xlrd

class runTest:
    def runAtpTest(self,testCaseFile):
        testCaseFile = os.path.join("/Users/zhouxin/PycharmProjects/testinterface/atpTestCase",testCaseFile)
        #print testCaseFile
        if not os.path.exists(testCaseFile):
            logging.error("测试用例文件不存在!")
            sys.exit()
        excel = xlrd.open_workbook(testCaseFile)
        return excel

    def runPaymentTest(self,testCaseFile):
        testCaseFile = os.path.join("/Users/zhouxin/PycharmProjects/testinterface/paymentTestCase",testCaseFile)
        #print testCaseFile
        if not os.path.exists(testCaseFile):
            logging.error("测试用例文件不存在!")
            sys.exit()
        excel = xlrd.open_workbook(testCaseFile)
        return excel

