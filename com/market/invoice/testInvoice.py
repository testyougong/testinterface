# -*- coding: utf-8 -*-
import json

import requests
import MySQLdb
import math
from com.market.main.Basic import Basic

invoiceNomalMoneyList = []
noInvoiceNomalMoneyList = []
invoiceActivityMoneyList = []
noInvoiceActivityMoneyList = []
invoiceBlackMoneyList = []
blackMoneyList = []

BasicApi = Basic()
token = BasicApi.login()  # 获取登录token
host = BasicApi.basic_url()  # 获取host
url = '/shopping/order/prepare'

params = {'sku_list':'[{"sku_id":"106306","qty":1},{"sku_id":"106309","qty":1},{"sku_id":"107740","qty":1},{"sku_id":"120899","qty":1}]','tab':1,'use_coupon':1,'use_cash_coupon':1,'token':token}
result = requests.post(host+url,params = params)
orderInfo = result.json()['content']['order_info']
#订单应付金额
money = float(orderInfo['money'])
moneyInfo = result.json()['content']['money_info']
#使用的现金券金额
couponCash = float(moneyInfo['cash_coupon_money'])
print "现金券金额:%.2f"%couponCash
#使用的优惠券金额
coupon = float(moneyInfo['ticket_coupon_money'])
print "优惠券金额:%.2f"%coupon
#接口计算出的可开票金额
invoiceMoney = float(moneyInfo['invoice_money'])
#满减金额
couponMoney = float(moneyInfo['coupon_money'])
if couponMoney == 0.00 :
    orderList = result.json()['content']['order_list']
    detailList = orderList[0]['detail_list']
    for i in detailList :
        if str(i['order_package_info']) :
            orderPackageInfo = i['order_package_info']
            for item in orderPackageInfo :
                packagePrice = float(item['package_price'])*float(item['qty'])
                sku_id = str(item['sku_id'])
                market = MySQLdb.connect(host='192.168.60.59', port=5200, user='root', passwd='', db='lsh_market_dev', charset="utf8")
                cursor = market.cursor(cursorclass=MySQLdb.cursors.DictCursor)
                sql = 'select * from sku_blacklist where sku_id = '+sku_id+''
                cursor.execute(sql)
                if (cursor.rowcount == 0):
                    if int(item['is_invoice']) == 1:
                        invoiceNomalMoneyList.append(packagePrice)
                    else:
                        noInvoiceNomalMoneyList.append(packagePrice)
                else:
                    blackMoneyList.append(packagePrice)
                    if int(item['is_invoice']) == 1:
                        invoiceBlackMoneyList.append(packagePrice)
        else:
            if str(i['black_tags']) == '[]':
                if int(i['is_invoice']) == 1 :
                    invoiceNomalMoneyList.append(float(i['placed_money']))
                else :
                    noInvoiceNomalMoneyList.append(float(i['placed_money']))
            else :
                blackMoneyList.append(float(i['placed_money']))
                if int(i['is_invoice']) == 1 :
                    invoiceBlackMoneyList.append(float(i['placed_money']))
    invoiceNomalMoney = sum(invoiceNomalMoneyList)
    noInvoiceNomalMoney = sum(noInvoiceNomalMoneyList)
    invoiceBlackMoney = sum(invoiceBlackMoneyList)
    blackMoney = sum(blackMoneyList)
    #最终可开票金额
    resultInvoiceMoney = invoiceNomalMoney - (((coupon + couponCash) / float(money + coupon + couponCash - blackMoney)) * invoiceNomalMoney ) + invoiceBlackMoney

    print "普通商品可开票金额:%.2f" % invoiceNomalMoney
    print "普通商品不可开票金额:%.2f" % noInvoiceNomalMoney
    print "黑名单商品可开票金额:%.2f" % invoiceBlackMoney
    print "应付金额:%.2f" % money
    print "后端计算出的最终可开票金额:%.2f" % invoiceMoney
    print "最终可开票金额:%.2f" % resultInvoiceMoney

else :
    orderList = result.json()['content']['order_list']
    detailList = orderList[0]['detail_list']
    for i in detailList:
        if str(i['order_package_info']) :
            orderPackageInfo = i['order_package_info']
            for item in orderPackageInfo :
                packagePrice = float(item['package_price'])*float(item['qty'])
                sku_id = str(item['sku_id'])
                market = MySQLdb.connect(host='192.168.60.59', port=5200, user='root', passwd='', db='lsh_market_dev', charset="utf8")
                cursor = market.cursor(cursorclass=MySQLdb.cursors.DictCursor)
                sql = 'select * from sku_blacklist where sku_id = '+sku_id+''
                cursor.execute(sql)
                if (cursor.rowcount == 0):
                    if int(item['is_invoice']) == 1:
                        invoiceNomalMoneyList.append(packagePrice)
                    else:
                        noInvoiceNomalMoneyList.append(packagePrice)
                else:
                    blackMoneyList.append(packagePrice)
                    if int(item['is_invoice']) == 1:
                        invoiceBlackMoneyList.append(packagePrice)
        else:
            if str(i['black_tags']) == '[]':
                tags = i['item_tags']
                if int(i['is_invoice']) == 1:
                    if str(tags) != '[]':
                        for tag in tags :
                            if tag['type'] == 4:
                                invoiceActivityMoneyList.append(float(i['placed_money']))
                            else:
                                invoiceNomalMoneyList.append(float(i['placed_money']))
                    else:
                        invoiceNomalMoneyList.append(float(i['placed_money']))
                else:
                    if str(tags) != '[]':
                        for tag in tags :
                            if tag['type'] == 4:
                                noInvoiceActivityMoneyList.append(float(i['placed_money']))
                            else :
                                noInvoiceNomalMoneyList.append(float(i['placed_money']))
                    else :
                        noInvoiceNomalMoneyList.append(float(i['placed_money']))
            else:
                blackMoneyList.append(float(i['placed_money']))
                if int(i['is_invoice']) == 1:
                    invoiceBlackMoneyList.append(float(i['placed_money']))
    invoiceNomalMoney = sum(invoiceNomalMoneyList)
    noInvoiceNomalMoney = sum(noInvoiceNomalMoneyList)
    invoiceBlackMoney = sum(invoiceBlackMoneyList)
    blackMoney = sum(blackMoneyList)
    invoiceActivityMoney = sum(invoiceActivityMoneyList)
    noInvoiceActivityMoney = sum(noInvoiceActivityMoneyList)
    activityMoney = invoiceActivityMoney + noInvoiceActivityMoney
    #满减金额分摊后的可开票金额
    resultInvoiceActivityMoney = invoiceActivityMoney - (couponMoney / float(activityMoney)) * invoiceActivityMoney
    # 普通商品可开票金额
    resultInvoiceNomalMoney = invoiceNomalMoney - ((coupon + couponCash) / float(money + coupon + couponCash + couponMoney - blackMoney)) * invoiceNomalMoney
    # 参与满减商品可开票金额
    resultCouponInvoiceActivityMoney = resultInvoiceActivityMoney - ((coupon + couponCash) / float(money + coupon + couponCash + couponMoney - blackMoney)) * invoiceActivityMoney
    # 最终可开票金额
    resultInvoiceMoney = resultInvoiceNomalMoney + resultCouponInvoiceActivityMoney + invoiceBlackMoney

    print "普通商品可开票金额:%.2f"%invoiceNomalMoney
    print "普通商品不可开票金额:%.2f"%noInvoiceNomalMoney
    print "满减商品可开票金额:%.2f"%invoiceActivityMoney
    print "满减商品不可开票金额:%.2f"%noInvoiceActivityMoney
    print "黑名单商品可开票金额:%.2f"%invoiceBlackMoney
    print "应付金额:%.2f"%money
    print "后端计算出的最终可开票金额:%.2f"%invoiceMoney
    print "最终可开票金额:%.2f"%resultInvoiceMoney


