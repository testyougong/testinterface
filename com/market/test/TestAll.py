# -*- coding: UTF-8 -*-
import os
import unittest
import HTMLTestRunner

from com.market.test.CartCalpricev2 import TestOrderCase1
from com.market.test.OrderPrepare import TestOrderCase2
from com.market.test.OrderInit import TestOrderCase3



class TestAll(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass


    def suite(self):
        suite = unittest.TestSuite()
        suite.addTest(TestOrderCase1("test_CartCalpricev2"))
        suite.addTest(TestOrderCase2("test_OrderPrepare"))
        suite.addTest(TestOrderCase3("test_OrderInit"))

        filename = "/Users/zhouxin/Desktop/result1.html"
        fp = file(filename, 'wb')
        runner = HTMLTestRunner.HTMLTestRunner(stream=fp, title="testing result", description="trying")
        runner.run(suite)
        fp.close()
        os.system(filename)

if __name__=='__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestAll.suite())
    unittest.TextTestRunner(verbosity=2).run(suite)