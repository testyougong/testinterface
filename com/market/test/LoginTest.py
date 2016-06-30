# -*- coding: UTF-8 -*-
import unittest

import requests
import xlrd

from com.market.main.Basic import Basic


class Login_Test(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass



    def test_login(self):
        BasicApi = Basic()
        url = BasicApi.basic_url()  # 获取url

        excel = xlrd.open_workbook('/Users/zhouxin/PycharmProjects/test/testcase.xlsx')
        sheet = excel.sheets()[1]
        nrows = sheet.nrows

        for i in range(1, nrows):  # 从第二行开始取
            username = sheet.cell(i,0).value
            password = sheet.cell(i,1).value

            user = {'username':int(username),'password':password}
            result = requests.post(url+'/user/info/login',params=user)
            assert result.status_code == 200
            if (result.json()['ret'] != ""):
                if(result.json()['ret'] == -10001 ):
                    self.assertEqual('账户或者密码错误,请重新登录'.decode('UTF-8'), result.json()['msg'])
                    print "接口 /user/info/login?username="+str(username)+"&password="+str(password)+"------------OK！"
                else:
                    self.assertEqual(0, result.json()['ret'])
                    assert result.json()['content']['uid'] == '8154237329960352984'
                    assert result.json()['content']['username'] == '13466640320'
                    assert result.json()['content']['token'] !=''
                    print "接口 /user/info/login?username="+str(username)+"&password="+str(password)+"------------OK！"
            else:
                print "接口 /user/info/login------------Failure！"
                self.assertEqual(0, result.json()['ret'])


if __name__ == "__main__":
    unittest.main()
