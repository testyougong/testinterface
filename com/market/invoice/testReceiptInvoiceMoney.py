# -*- coding: utf-8 -*-
import json

import requests
import MySQLdb
from com.market.main.Basic import Basic

invoiceNomalMoneyListR0 = []
invoiceNomalMoneyListR13 = []
invoiceNomalMoneyListR17 = []
noInvoiceNomalMoneyList = []

invoiceActivityMoneyListR0 = []
invoiceActivityMoneyListR13 = []
invoiceActivityMoneyListR17 = []
noInvoiceActivityMoneyList = []

invoiceActivity2MoneyListR0 = []
invoiceActivity2MoneyListR13 = []
invoiceActivity2MoneyListR17 = []
noInvoiceActivity2MoneyList = []

invoiceActivity3MoneyListR0 = []
invoiceActivity3MoneyListR13 = []
invoiceActivity3MoneyListR17 = []
noInvoiceActivity3MoneyList = []

invoiceBlackMoneyListR0 = []
invoiceBlackMoneyListR13 = []
invoiceBlackMoneyListR17 = []
noInvoiceBlackMoneyList = []

BasicApi = Basic()
cookie = BasicApi.mis_login()
host = BasicApi.mis_url()  # 获取host
orderId = 6253476612856094720
url = '/order/user/view?order_id='+str(orderId)+'&format=json'
headers = {'Cookie':'MISSESSID=8hvc8gpn5fh5cserkqnnit7d54; zone_id=1000'}
result = requests.get(host + url,headers=headers)

receiptList = result.json()['content']['receipt_list']
receiptListHeadInfo = receiptList[0]['head_info']
headInfo = receiptListHeadInfo['ext']['head_info']
#订单应付金额(要加上售后金额)
money = float(headInfo['money']) + float(receiptListHeadInfo['afs_money'])
#现金券金额
cashCouponMoney = float(headInfo['cash_coupon_money'])
print "现金券金额:%.2f"%cashCouponMoney
#优惠券金额
ticketCouponMoney = float(headInfo['ticket_coupon_money'])
print "优惠券金额:%.2f"%ticketCouponMoney
#抹零金额
floorMoney = float(headInfo['floor_money'])
print "抹零金额：%.2f"%floorMoney

if str(headInfo['activity_info']) != '[]':
    activityList = []
    activityList2 = []
    activityList3 = []
    couponMoneyList = []
    activityIdList = []
    for row in json.loads(headInfo['activity_info']):
        #满减金额
        couponMoney = float(row['coupon_money'])
        print "满减金额:%.2f"%couponMoney
        couponMoneyList.append(couponMoney)
        activityId = str(row['info']['id'])
        activityIdList.append(activityId)

    for row in json.loads(headInfo['activity_info']):
        for j in row['sku_list'] :
            skuId = j['sku_id']
            market = MySQLdb.connect(host='192.168.60.59', port=5200, user='root', db='lsh_market_dev',charset="utf8")
            cursor = market.cursor(cursorclass=MySQLdb.cursors.DictCursor)
            sql = 'select activity_info from order_sku where order_id = {0} and sku_id = {1}'.format(orderId, skuId)
            #for sku in row['sku_list']:
            cursor.execute(sql)
            data = cursor.fetchall()
            for activityInfo in data:
                for row in json.loads(activityInfo['activity_info']):
                    id =  str(row['info']['id'])
                    if id == activityIdList[0]:
                        activityList.append(skuId)
                    elif id == activityIdList[1]:
                        activityList2.append(skuId)
                    else :
                        activityList3.append(skuId)
    #print couponMoneyList
    #print activityList
    #print activityList
    #print activityList2
    #print activityList3
    detailList = receiptList[0]['detail_list']
    for i in detailList :
        if ('package_info' in i.keys()) and (str(i['tags']) == "[u'\u5957\u9910\u5355\u54c1']".decode('UTF-8')):
            skuId = i['sku_id']
            packageId = i['package_id']
            price = float(i['price'])
            qty = float(i['qty'])
            market = MySQLdb.connect(host='192.168.60.59', port=5200, user='root', db='lsh_market_dev',charset="utf8")
            cursor = market.cursor(cursorclass=MySQLdb.cursors.DictCursor)
            sql = 'select is_invoice,invoice_rate,is_blacklist from order_sku where order_id = {0} and sku_id = {1} and package_id = {2}'.format(orderId, skuId,packageId)
            cursor.execute(sql)
            data = cursor.fetchall()
            market.close()
            for invoice in data:
                if invoice['is_blacklist'] == 1:
                    if invoice['is_invoice'] == 1 and invoice['invoice_rate'] == 1:
                        invoiceBlackMoneyListR0.append(price*qty)
                    elif invoice['is_invoice'] == 1 and invoice['invoice_rate'] == 2:
                        invoiceBlackMoneyListR13.append(price*qty)
                    elif invoice['is_invoice'] == 1 and invoice['invoice_rate'] == 3:
                        invoiceBlackMoneyListR17.append(price*qty)
                    else:
                        noInvoiceBlackMoneyList.append(price*qty)
                else:
                    if invoice['is_invoice'] == 1 and invoice['invoice_rate'] == 1:
                        invoiceNomalMoneyListR0.append(price*qty)
                    elif invoice['is_invoice'] == 1 and invoice['invoice_rate'] == 2:
                        invoiceNomalMoneyListR13.append(price*qty)
                    elif invoice['is_invoice'] == 1 and invoice['invoice_rate'] == 3:
                        invoiceNomalMoneyListR17.append(price*qty)
                    else:
                        noInvoiceNomalMoneyList.append(price*qty)

        elif ('package_info' in i.keys()) and (str(i['tags']) == "[u'\u5957\u9910']".decode('UTF-8')):
            itemList = i['package_info']['item_list']
            for item in itemList:
                skuId = item['sku_id']
                packageId = item['package_id']
                price = float(item['package_price'])
                qty = float(item['qty'])
                market = MySQLdb.connect(host='192.168.60.59', port=5200, user='root', db='lsh_market_dev',charset="utf8")
                cursor = market.cursor(cursorclass=MySQLdb.cursors.DictCursor)
                sql = 'select is_invoice,invoice_rate,is_blacklist from order_sku where order_id = {0} and sku_id = {1} and package_id = {2}'.format(orderId, skuId , packageId)
                cursor.execute(sql)
                data = cursor.fetchall()
                for invoice in data:
                    if invoice['is_blacklist'] == 1:
                        if invoice['is_invoice'] == 1 and invoice['invoice_rate'] == 1:
                            invoiceBlackMoneyListR0.append(price*qty)
                        elif invoice['is_invoice'] == 1 and invoice['invoice_rate'] == 2:
                            invoiceBlackMoneyListR13.append(price*qty)
                        elif invoice['is_invoice'] == 1 and invoice['invoice_rate'] == 3:
                            invoiceBlackMoneyListR17.append(price*qty)
                        else:
                            noInvoiceBlackMoneyList.append(price*qty)
                    else:
                        if invoice['is_invoice'] == 1 and invoice['invoice_rate'] == 1:
                            invoiceNomalMoneyListR0.append(price*qty)
                        elif invoice['is_invoice'] == 1 and invoice['invoice_rate'] == 2:
                            invoiceNomalMoneyListR13.append(price*qty)
                        elif invoice['is_invoice'] == 1 and invoice['invoice_rate'] == 3:
                            invoiceNomalMoneyListR17.append(price*qty)
                        else:
                            noInvoiceNomalMoneyList.append(price*qty)
        else :
            skuId = int(i['sku_id'])
            market = MySQLdb.connect(host='192.168.60.59', port=5200, user='root', db='lsh_market_dev',charset="utf8")
            cursor = market.cursor(cursorclass=MySQLdb.cursors.DictCursor)
            sql = 'select is_invoice,invoice_rate,is_blacklist from order_sku where order_id = {0} and sku_id = {1}'.format(orderId,skuId)
            cursor.execute(sql)
            data = cursor.fetchall()
            market.close()
            if skuId in activityList:
                for invoice in data :
                    if invoice['is_invoice'] == 1 and invoice['invoice_rate'] == 1:
                        invoiceActivityMoneyListR0.append(float(i['money']))
                    elif invoice['is_invoice'] == 1 and invoice['invoice_rate'] == 2:
                        invoiceActivityMoneyListR13.append(float(i['money']))
                    elif invoice['is_invoice'] == 1 and invoice['invoice_rate'] == 3:
                        invoiceActivityMoneyListR17.append(float(i['money']))
                    else :
                        noInvoiceActivityMoneyList.append(float(i['money']))
            elif skuId in activityList2:
                for invoice in data :
                    if invoice['is_invoice'] == 1 and invoice['invoice_rate'] == 1:
                        invoiceActivity2MoneyListR0.append(float(i['money']))
                    elif invoice['is_invoice'] == 1 and invoice['invoice_rate'] == 2:
                        invoiceActivity2MoneyListR13.append(float(i['money']))
                    elif invoice['is_invoice'] == 1 and invoice['invoice_rate'] == 3:
                        invoiceActivity2MoneyListR17.append(float(i['money']))
                    else :
                        noInvoiceActivity2MoneyList.append(float(i['money']))
            elif skuId in activityList3:
                for invoice in data :
                    if invoice['is_invoice'] == 1 and invoice['invoice_rate'] == 1:
                        invoiceActivity3MoneyListR0.append(float(i['money']))
                    elif invoice['is_invoice'] == 1 and invoice['invoice_rate'] == 2:
                        invoiceActivity3MoneyListR13.append(float(i['money']))
                    elif invoice['is_invoice'] == 1 and invoice['invoice_rate'] == 3:
                        invoiceActivity3MoneyListR17.append(float(i['money']))
                    else :
                        noInvoiceActivity3MoneyList.append(float(i['money']))
            else :
                for invoice in data :
                    if invoice['is_blacklist'] == 1 :
                        if invoice['is_invoice'] == 1 and invoice['invoice_rate'] == 1:
                            invoiceBlackMoneyListR0.append(float(i['money']))
                        elif invoice['is_invoice'] == 1 and invoice['invoice_rate'] == 2:
                            invoiceBlackMoneyListR13.append(float(i['money']))
                        elif invoice['is_invoice'] == 1 and invoice['invoice_rate'] == 3:
                            invoiceBlackMoneyListR17.append(float(i['money']))
                        else :
                            noInvoiceBlackMoneyList.append(float(i['money']))
                    else :
                        if invoice['is_invoice'] == 1 and invoice['invoice_rate'] == 1:
                            invoiceNomalMoneyListR0.append(float(i['money']))
                        elif invoice['is_invoice'] == 1 and invoice['invoice_rate'] == 2:
                            invoiceNomalMoneyListR13.append(float(i['money']))
                        elif invoice['is_invoice'] == 1 and invoice['invoice_rate'] == 3:
                            invoiceNomalMoneyListR17.append(float(i['money']))
                        else :
                            noInvoiceNomalMoneyList.append(float(i['money']))
    # 各税率黑名单商品可开票金额
    invoiceBlackMoneyR0 = sum(invoiceBlackMoneyListR0)
    invoiceBlackMoneyR13 = sum(invoiceBlackMoneyListR13)
    invoiceBlackMoneyR17 = sum(invoiceBlackMoneyListR17)
    noInvoiceBlackMoney = sum(noInvoiceBlackMoneyList)
    # 各税率黑名单商品最终可开票金额
    resultInvoiceBlackMoneyR0 = invoiceBlackMoneyR0 - (floorMoney/float(money + cashCouponMoney + ticketCouponMoney + couponMoney + floorMoney))*invoiceBlackMoneyR0
    resultInvoiceBlackMoneyR13 = invoiceBlackMoneyR13 - (floorMoney / float(money + cashCouponMoney + ticketCouponMoney + couponMoney + floorMoney)) * invoiceBlackMoneyR13
    resultInvoiceBlackMoneyR17 = invoiceBlackMoneyR17 - (floorMoney / float(money + cashCouponMoney + ticketCouponMoney + couponMoney + floorMoney)) * invoiceBlackMoneyR17
    blackMoney = invoiceBlackMoneyR0 + invoiceBlackMoneyR13 + invoiceBlackMoneyR17 + noInvoiceBlackMoney
    #满减金额总和
    couponMoney = sum(couponMoneyList)
    invoiceActivityMoneyR0 = sum(invoiceActivityMoneyListR0)
    invoiceActivityMoneyR13 = sum(invoiceActivityMoneyListR13)
    invoiceActivityMoneyR17 = sum(invoiceActivityMoneyListR17)
    noInvoiceActivityMoney = sum(noInvoiceActivityMoneyList)
    activityMoney = invoiceActivityMoneyR0 + invoiceActivityMoneyR13 + invoiceActivityMoneyR17 + noInvoiceActivityMoney
    # 满减活动1金额分摊后满减后各税率商品的可开票金额
    resultInvoiceActivityMoneyR0 = invoiceActivityMoneyR0 - (couponMoneyList[0] / float(activityMoney)) * invoiceActivityMoneyR0
    resultInvoiceActivityMoneyR13 = invoiceActivityMoneyR13 - (couponMoneyList[0] / float(activityMoney)) * invoiceActivityMoneyR13
    resultInvoiceActivityMoneyR17 = invoiceActivityMoneyR17 - (couponMoneyList[0] / float(activityMoney)) * invoiceActivityMoneyR17

    # 满减活动1金额分摊后优惠券后各税率商品的可开票金额
    resultCouponInvoiceActivityMoneyR0 = resultInvoiceActivityMoneyR0 - ((cashCouponMoney + ticketCouponMoney) / float(money + cashCouponMoney + ticketCouponMoney + couponMoney + floorMoney - blackMoney)) * invoiceActivityMoneyR0 - (floorMoney / float(money + cashCouponMoney + ticketCouponMoney + couponMoney + floorMoney)) * invoiceActivityMoneyR0
    resultCouponInvoiceActivityMoneyR13 = resultInvoiceActivityMoneyR13 - ((cashCouponMoney + ticketCouponMoney) / float(money + cashCouponMoney + ticketCouponMoney + couponMoney + floorMoney - blackMoney)) * invoiceActivityMoneyR13 - (floorMoney / float(money + cashCouponMoney + ticketCouponMoney + couponMoney + floorMoney)) * invoiceActivityMoneyR13
    resultCouponInvoiceActivityMoneyR17 = resultInvoiceActivityMoneyR17 - ((cashCouponMoney + ticketCouponMoney) / float(money + cashCouponMoney + ticketCouponMoney + couponMoney + floorMoney - blackMoney)) * invoiceActivityMoneyR17 - (floorMoney / float(money + cashCouponMoney + ticketCouponMoney + couponMoney + floorMoney)) * invoiceActivityMoneyR17

    try:
        invoiceActivity2MoneyR0 = sum(invoiceActivity2MoneyListR0)
        invoiceActivity2MoneyR13 = sum(invoiceActivity2MoneyListR13)
        invoiceActivity2MoneyR17 = sum(invoiceActivity2MoneyListR17)
        noInvoiceActivity2Money = sum(noInvoiceActivity2MoneyList)
        activity2Money = invoiceActivity2MoneyR0 + invoiceActivity2MoneyR13 + invoiceActivity2MoneyR17 + noInvoiceActivity2Money
        # 满减活动2金额分摊后满减后各税率商品的可开票金额
        resultInvoiceActivity2MoneyR0 = invoiceActivity2MoneyR0 - (couponMoneyList[1] / float(activity2Money)) * invoiceActivity2MoneyR0
        resultInvoiceActivity2MoneyR13 = invoiceActivity2MoneyR13 - (couponMoneyList[1] / float(activity2Money)) * invoiceActivity2MoneyR13
        resultInvoiceActivity2MoneyR17 = invoiceActivity2MoneyR17 - (couponMoneyList[1] / float(activity2Money)) * invoiceActivity2MoneyR17
        # 满减活动2金额分摊后优惠券后各税率商品的可开票金额
        resultCouponInvoiceActivity2MoneyR0 = resultInvoiceActivity2MoneyR0 - ((cashCouponMoney + ticketCouponMoney) / float(money + cashCouponMoney + ticketCouponMoney + couponMoney + floorMoney - blackMoney)) * invoiceActivity2MoneyR0 - (floorMoney / float(money + cashCouponMoney + ticketCouponMoney + couponMoney + floorMoney)) * invoiceActivity2MoneyR0
        resultCouponInvoiceActivity2MoneyR13 = resultInvoiceActivity2MoneyR13 - ((cashCouponMoney + ticketCouponMoney) / float(money + cashCouponMoney + ticketCouponMoney + couponMoney + floorMoney - blackMoney)) * invoiceActivity2MoneyR13 - (floorMoney / float(money + cashCouponMoney + ticketCouponMoney + couponMoney + floorMoney)) * invoiceActivity2MoneyR13
        resultCouponInvoiceActivity2MoneyR17 = resultInvoiceActivity2MoneyR17 - ((cashCouponMoney + ticketCouponMoney) / float(money + cashCouponMoney + ticketCouponMoney + couponMoney + floorMoney - blackMoney)) * invoiceActivity2MoneyR17 - (floorMoney / float(money + cashCouponMoney + ticketCouponMoney + couponMoney + floorMoney)) * invoiceActivity2MoneyR17
    except:
        print "只有%d个满减活动"%len(activityIdList)
        resultCouponInvoiceActivity2MoneyR0 = 0
        resultCouponInvoiceActivity2MoneyR13 = 0
        resultCouponInvoiceActivity2MoneyR17 = 0

    try:
        invoiceActivity3MoneyR0 = sum(invoiceActivity3MoneyListR0)
        invoiceActivity3MoneyR13 = sum(invoiceActivity3MoneyListR13)
        invoiceActivity3MoneyR17 = sum(invoiceActivity3MoneyListR17)
        noInvoiceActivity3Money = sum(noInvoiceActivity3MoneyList)
        activity3Money = invoiceActivity3MoneyR0 + invoiceActivity3MoneyR13 + invoiceActivity3MoneyR17 + noInvoiceActivity3Money
        # 满减活动3金额分摊后满减后各税率商品的可开票金额
        resultInvoiceActivity3MoneyR0 = invoiceActivity3MoneyR0 - (couponMoneyList[2] / float(activity3Money)) * invoiceActivity3MoneyR0
        resultInvoiceActivity3MoneyR13 = invoiceActivity3MoneyR13 - (couponMoneyList[2] / float(activity3Money)) * invoiceActivity3MoneyR13
        resultInvoiceActivity3MoneyR17 = invoiceActivity3MoneyR17 - (couponMoneyList[2] / float(activity3Money)) * invoiceActivity3MoneyR17
        # 满减活动2金额分摊后优惠券后各税率商品的可开票金额
        resultCouponInvoiceActivity3MoneyR0 = resultInvoiceActivity3MoneyR0 - ((cashCouponMoney + ticketCouponMoney) / float(money + cashCouponMoney + ticketCouponMoney + couponMoney + floorMoney - blackMoney)) * invoiceActivity3MoneyR0 - (floorMoney / float(money + cashCouponMoney + ticketCouponMoney + couponMoney + floorMoney)) * invoiceActivity3MoneyR0
        resultCouponInvoiceActivity3MoneyR13 = resultInvoiceActivity3MoneyR13 - ((cashCouponMoney + ticketCouponMoney) / float(money + cashCouponMoney + ticketCouponMoney + couponMoney + floorMoney - blackMoney)) * invoiceActivity3MoneyR13 - (floorMoney / float(money + cashCouponMoney + ticketCouponMoney + couponMoney + floorMoney)) * invoiceActivity3MoneyR13
        resultCouponInvoiceActivity3MoneyR17 = resultInvoiceActivity3MoneyR17 - ((cashCouponMoney + ticketCouponMoney) / float(money + cashCouponMoney + ticketCouponMoney + couponMoney + floorMoney - blackMoney)) * invoiceActivity3MoneyR17 - (floorMoney / float(money + cashCouponMoney + ticketCouponMoney + couponMoney + floorMoney)) * invoiceActivity3MoneyR17
    except:
        print "只有%d个满减活动"%len(activityIdList)
        resultCouponInvoiceActivity3MoneyR0 = 0
        resultCouponInvoiceActivity3MoneyR13 = 0
        resultCouponInvoiceActivity3MoneyR17 = 0

    invoiceNomalMoneyR0 = sum(invoiceNomalMoneyListR0)
    invoiceNomalMoneyR13 = sum(invoiceNomalMoneyListR13)
    invoiceNomalMoneyR17 = sum(invoiceNomalMoneyListR17)
    noInvoiceNomalMoney = sum(noInvoiceNomalMoneyList)
    # 各税率普通商品可开票金额
    resultInvoiceNomalMoneyRO = invoiceNomalMoneyR0 - ((cashCouponMoney + ticketCouponMoney) / float(money + cashCouponMoney + ticketCouponMoney + couponMoney + floorMoney - blackMoney)) * invoiceNomalMoneyR0 - (floorMoney / float(money + cashCouponMoney + ticketCouponMoney + couponMoney + floorMoney)) * invoiceNomalMoneyR0
    resultInvoiceNomalMoneyR13 = invoiceNomalMoneyR13 - ((cashCouponMoney + ticketCouponMoney) / float(money + cashCouponMoney + ticketCouponMoney + couponMoney + floorMoney - blackMoney)) * invoiceNomalMoneyR13 - (floorMoney / float(money + cashCouponMoney + ticketCouponMoney + couponMoney + floorMoney)) * invoiceNomalMoneyR13
    resultInvoiceNomalMoneyR17 = invoiceNomalMoneyR17 - ((cashCouponMoney + ticketCouponMoney) / float(money + cashCouponMoney + ticketCouponMoney + couponMoney + floorMoney - blackMoney)) * invoiceNomalMoneyR17 - (floorMoney / float(money + cashCouponMoney + ticketCouponMoney + couponMoney + floorMoney)) * invoiceNomalMoneyR17
    resultInvoiceNomalMoney = resultInvoiceNomalMoneyRO + resultInvoiceNomalMoneyR13 + resultInvoiceNomalMoneyR17

    # 各税率最终可开票金额
    resultInvoiceMoneyR0 = resultCouponInvoiceActivityMoneyR0 + resultCouponInvoiceActivity2MoneyR0 + resultCouponInvoiceActivity3MoneyR0 + resultInvoiceBlackMoneyR0 + resultInvoiceNomalMoneyRO
    resultInvoiceMoneyR13 = resultCouponInvoiceActivityMoneyR13 + resultCouponInvoiceActivity2MoneyR13 + resultCouponInvoiceActivity3MoneyR13 +resultInvoiceBlackMoneyR13 + resultInvoiceNomalMoneyR13
    resultInvoiceMoneyR17 = resultCouponInvoiceActivityMoneyR17 + resultCouponInvoiceActivity2MoneyR17 + resultCouponInvoiceActivity3MoneyR17 + resultInvoiceBlackMoneyR17 + resultInvoiceNomalMoneyR17
    # 最终可开票金额
    resultInvoiceMoney = resultInvoiceMoneyR0 + resultInvoiceMoneyR13 + resultInvoiceMoneyR17
else:
    couponMoney = 0
    print "满减金额:%.2f" % couponMoney
    detailList = receiptList[0]['detail_list']
    for i in detailList:
        if ('package_info' in i.keys()) and (str(i['tags']) == "[u'\u5957\u9910\u5355\u54c1']".decode('UTF-8')):
            skuId = i['sku_id']
            packageId = i['package_id']
            price = float(i['price'])
            qty = float(i['qty'])
            market = MySQLdb.connect(host='192.168.60.59', port=5200, user='root', db='lsh_market_dev',charset="utf8")
            cursor = market.cursor(cursorclass=MySQLdb.cursors.DictCursor)
            sql = 'select is_invoice,invoice_rate,is_blacklist from order_sku where order_id = {0} and sku_id = {1} and package_id = {2}'.format(orderId, skuId,packageId)
            cursor.execute(sql)
            data = cursor.fetchall()
            market.close()
            for invoice in data:
                if invoice['is_blacklist'] == 1:
                    if invoice['is_invoice'] == 1 and invoice['invoice_rate'] == 1:
                        invoiceBlackMoneyListR0.append(price*qty)
                    elif invoice['is_invoice'] == 1 and invoice['invoice_rate'] == 2:
                        invoiceBlackMoneyListR13.append(price*qty)
                    elif invoice['is_invoice'] == 1 and invoice['invoice_rate'] == 3:
                        invoiceBlackMoneyListR17.append(price*qty)
                    else:
                        noInvoiceBlackMoneyList.append(price*qty)
                else:
                    if invoice['is_invoice'] == 1 and invoice['invoice_rate'] == 1:
                        invoiceNomalMoneyListR0.append(price*qty)
                    elif invoice['is_invoice'] == 1 and invoice['invoice_rate'] == 2:
                        invoiceNomalMoneyListR13.append(price*qty)
                    elif invoice['is_invoice'] == 1 and invoice['invoice_rate'] == 3:
                        invoiceNomalMoneyListR17.append(price*qty)
                    else:
                        noInvoiceNomalMoneyList.append(price*qty)
        elif ('package_info' in i.keys()) and (str(i['tags']) == "[u'\u5957\u9910']".decode('UTF-8')):
            itemList = i['package_info']['item_list']
            for item in itemList:
                skuId = item['sku_id']
                packageId = item['package_id']
                market = MySQLdb.connect(host='192.168.60.59', port=5200, user='root', db='lsh_market_dev',charset="utf8")
                cursor = market.cursor(cursorclass=MySQLdb.cursors.DictCursor)
                sql = 'select is_invoice,invoice_rate,is_blacklist from order_sku where order_id = {0} and sku_id = {1} and package_id = {2}'.format(orderId, skuId , packageId)
                cursor.execute(sql)
                data = cursor.fetchall()
                for invoice in data:
                    if invoice['is_blacklist'] == 1:
                        if invoice['is_invoice'] == 1 and invoice['invoice_rate'] == 1:
                            invoiceBlackMoneyListR0.append(float(item['package_price']))
                        elif invoice['is_invoice'] == 1 and invoice['invoice_rate'] == 2:
                            invoiceBlackMoneyListR13.append(float(item['package_price']))
                        elif invoice['is_invoice'] == 1 and invoice['invoice_rate'] == 3:
                            invoiceBlackMoneyListR17.append(float(item['package_price']))
                        else:
                            noInvoiceBlackMoneyList.append(float(item['package_price']))
                    else:
                        if invoice['is_invoice'] == 1 and invoice['invoice_rate'] == 1:
                            invoiceNomalMoneyListR0.append(float(item['package_price']))
                        elif invoice['is_invoice'] == 1 and invoice['invoice_rate'] == 2:
                            invoiceNomalMoneyListR13.append(float(item['package_price']))
                        elif invoice['is_invoice'] == 1 and invoice['invoice_rate'] == 3:
                            invoiceNomalMoneyListR17.append(float(item['package_price']))
                        else:
                            noInvoiceNomalMoneyList.append(float(item['package_price']))
        else:
            skuId = i['sku_id']
            market = MySQLdb.connect(host='192.168.60.59', port=5200, user='root', db='lsh_market_dev', charset="utf8")
            cursor = market.cursor(cursorclass=MySQLdb.cursors.DictCursor)
            sql = 'select is_invoice,invoice_rate,is_blacklist from order_sku where order_id = {0} and sku_id = {1} and package_id = ""'.format(orderId, skuId)
            cursor.execute(sql)
            data = cursor.fetchall()
            market.close()
            for invoice in data:
                if invoice['is_blacklist'] == 1:
                    if invoice['is_invoice'] == 1 and invoice['invoice_rate'] == 1:
                        invoiceBlackMoneyListR0.append(float(i['money']))
                    elif invoice['is_invoice'] == 1 and invoice['invoice_rate'] == 2:
                        invoiceBlackMoneyListR13.append(float(i['money']))
                    elif invoice['is_invoice'] == 1 and invoice['invoice_rate'] == 3:
                        invoiceBlackMoneyListR17.append(float(i['money']))
                    else:
                        noInvoiceBlackMoneyList.append(float(i['money']))
                else:
                    if invoice['is_invoice'] == 1 and invoice['invoice_rate'] == 1:
                        invoiceNomalMoneyListR0.append(float(i['money']))
                    elif invoice['is_invoice'] == 1 and invoice['invoice_rate'] == 2:
                        invoiceNomalMoneyListR13.append(float(i['money']))
                    elif invoice['is_invoice'] == 1 and invoice['invoice_rate'] == 3:
                        invoiceNomalMoneyListR17.append(float(i['money']))
                    else:
                        noInvoiceNomalMoneyList.append(float(i['money']))
    #各税率满减商品可开票金额
    invoiceActivityMoneyR0 = 0
    invoiceActivityMoneyR13 = 0
    invoiceActivityMoneyR17 = 0
    noInvoiceActivityMoney = 0

    invoiceActivity2MoneyR0 = 0
    invoiceActivity2MoneyR13 = 0
    invoiceActivity2MoneyR17 = 0
    noInvoiceActivity2Money = 0

    invoiceActivity3MoneyR0 = 0
    invoiceActivity3MoneyR13 = 0
    invoiceActivity3MoneyR17 = 0
    noInvoiceActivity3Money = 0

    # 各税率黑名单商品可开票金额
    invoiceBlackMoneyR0 = sum(invoiceBlackMoneyListR0)
    invoiceBlackMoneyR13 = sum(invoiceBlackMoneyListR13)
    invoiceBlackMoneyR17 = sum(invoiceBlackMoneyListR17)
    noInvoiceBlackMoney = sum(noInvoiceBlackMoneyList)
    # 各税率黑名单商品最终可开票金额
    resultInvoiceBlackMoneyR0 = invoiceBlackMoneyR0 - (floorMoney / float(money + cashCouponMoney + ticketCouponMoney + couponMoney + floorMoney)) * invoiceBlackMoneyR0
    resultInvoiceBlackMoneyR13 = invoiceBlackMoneyR13 - (floorMoney / float(money + cashCouponMoney + ticketCouponMoney + couponMoney + floorMoney)) * invoiceBlackMoneyR13
    resultInvoiceBlackMoneyR17 = invoiceBlackMoneyR17 - (floorMoney / float(money + cashCouponMoney + ticketCouponMoney + couponMoney + floorMoney)) * invoiceBlackMoneyR17
    blackMoney = invoiceBlackMoneyR0 + invoiceBlackMoneyR13 + invoiceBlackMoneyR17 + noInvoiceBlackMoney

    invoiceNomalMoneyR0 = sum(invoiceNomalMoneyListR0)
    invoiceNomalMoneyR13 = sum(invoiceNomalMoneyListR13)
    invoiceNomalMoneyR17 = sum(invoiceNomalMoneyListR17)
    noInvoiceNomalMoney = sum(noInvoiceNomalMoneyList)
    # 各税率普通商品可开票金额
    resultInvoiceNomalMoneyRO = invoiceNomalMoneyR0 - ((cashCouponMoney + ticketCouponMoney) / float(money + cashCouponMoney + ticketCouponMoney + floorMoney - blackMoney)) * invoiceNomalMoneyR0 - (floorMoney / float(money + cashCouponMoney + ticketCouponMoney + couponMoney + floorMoney)) * invoiceNomalMoneyR0
    resultInvoiceNomalMoneyR13 = invoiceNomalMoneyR13 - ((cashCouponMoney + ticketCouponMoney) / float(money + cashCouponMoney + ticketCouponMoney + floorMoney - blackMoney)) * invoiceNomalMoneyR13 - (floorMoney / float(money + cashCouponMoney + ticketCouponMoney + couponMoney + floorMoney)) * invoiceNomalMoneyR13
    resultInvoiceNomalMoneyR17 = invoiceNomalMoneyR17 - ((cashCouponMoney + ticketCouponMoney) / float(money + cashCouponMoney + ticketCouponMoney + floorMoney - blackMoney)) * invoiceNomalMoneyR17 - (floorMoney / float(money + cashCouponMoney + ticketCouponMoney + couponMoney + floorMoney)) * invoiceNomalMoneyR17
    resultInvoiceNomalMoney = resultInvoiceNomalMoneyRO + resultInvoiceNomalMoneyR13 + resultInvoiceNomalMoneyR17

    # 各税率最终可开票金额
    resultInvoiceMoneyR0 = resultInvoiceBlackMoneyR0 + resultInvoiceNomalMoneyRO
    resultInvoiceMoneyR13 = resultInvoiceBlackMoneyR13 + resultInvoiceNomalMoneyR13
    resultInvoiceMoneyR17 = resultInvoiceBlackMoneyR17 + resultInvoiceNomalMoneyR17
    # 最终可开票金额
    resultInvoiceMoney = resultInvoiceMoneyR0 + resultInvoiceMoneyR13 + resultInvoiceMoneyR17

print "0%"+"税率满减活动1商品金额:%.2f"%invoiceActivityMoneyR0
print "13%"+"税率满减活动1商品金额:%.2f"%invoiceActivityMoneyR13
print "17%"+"税率满减活动1商品金额:%.2f"%invoiceActivityMoneyR17
print "不可开票的满减活动1商品金额:%.2f"%noInvoiceActivityMoney
print "0%"+"税率满减活动2商品金额:%.2f"%invoiceActivity2MoneyR0
print "13%"+"税率满减活动2商品金额:%.2f"%invoiceActivity2MoneyR13
print "17%"+"税率满减活动2商品金额:%.2f"%invoiceActivity2MoneyR17
print "不可开票的满减活动2商品金额:%.2f"%noInvoiceActivity2Money
print "0%"+"税率满减活动3商品金额:%.2f"%invoiceActivity3MoneyR0
print "13%"+"税率满减活动3商品金额:%.2f"%invoiceActivity3MoneyR13
print "17%"+"税率满减活动3商品金额:%.2f"%invoiceActivity3MoneyR17
print "不可开票的满减活动3商品金额:%.2f"%noInvoiceActivity3Money
print "0%"+"税率普通商品金额:%.2f"%invoiceNomalMoneyR0
print "13%"+"税率普通商品金额:%.2f"%invoiceNomalMoneyR13
print "17%"+"税率普通商品金额:%.2f"%invoiceNomalMoneyR17
print "不可开票的普通商品金额:%.2f"%noInvoiceNomalMoney
print "0%"+"税率黑名单商品金额:%.2f"%invoiceBlackMoneyR0
print "13%"+"税率黑名单商品金额:%.2f"%invoiceBlackMoneyR13
print "17%"+"税率黑名单商品金额:%.2f"%invoiceBlackMoneyR17
print "不可开票的黑名单商品金额:%.2f"%noInvoiceBlackMoney

print "0%"+"税率可开票金额:%.2f"%resultInvoiceMoneyR0
print "13%"+"税率可开票金额:%.2f"%resultInvoiceMoneyR13
print "17%"+"税率可开票金额:%.2f"%resultInvoiceMoneyR17
print "最终可开票金额:%.2f"%resultInvoiceMoney

