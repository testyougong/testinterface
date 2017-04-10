import unittest

from com.market.main.MySQLdb import MySQLdb

class test(unittest.TestCase):
    def test1(self):
        dbtest = MySQLdb()
        dbtest.MySQL("'select sku_id from item_sale limit 10'")

if __name__ == "__main__":
    unittest.main()
