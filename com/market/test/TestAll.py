# -*- coding: UTF-8 -*-
import os
import unittest

import HTMLTestRunner

from com.market.test.LoginTest import Login_Test
from com.market.test.SkuGetlistTest import SkuGetlistTest


class TestAll(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

        @staticmethod
        def suite():
            test = unittest.TestSuite()
            test.addTest(Login_Test("test_login"))
            test.addTest(SkuGetlistTest("test_skugetlist"))


            filename = "/Users/zhouxin/Desktop/result1.html"
            fp = file(filename, 'wb')
            runner = HTMLTestRunner.HTMLTestRunner(stream=fp,title="testing result",description="trying")
            runner.run(suite())
            fp.close()
            os.system(filename)

if __name__=='__main__':
    unittest.TextTestRunner(verbosity=2).run(TestAll.suite())