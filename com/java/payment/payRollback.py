# -*- coding: utf-8 -*-
import MySQLdb

order_code = raw_input("请输入订单号:")

#更改oms中订单状态为"已发货",变更为32
omsConn = MySQLdb.Connect(host='192.168.60.59', port=5200, user='root', passwd='', db='lsh_oms', charset="utf8")
omsCursor = omsConn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
try:
    omsCursor.execute("update order_head set order_status = 32 where order_code = {0}".format(order_code))
    omsConn.commit()
    if (omsCursor.rowcount != 1):
        print "订单状态回滚失败",
        omsCursor.execute("select order_status from order_head where order_code = {0}".format(order_code))
        oms_status = omsCursor.fetchall()[0]['order_status']
        print "当前订单状态为:" + str(oms_status)
    else :
        print "订单状态回滚完成"
except Exception,e:
    print Exception,":",e
    omsConn.rollback()
omsCursor.close()
omsConn.close()

#更改tms中发货单状态为"配送中",变更为1
tmsConn = MySQLdb.Connect(host='192.168.60.59', port=5200, user='root', passwd='', db='lsh_tms_66', charset="utf8")
tmsCursor = tmsConn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
try:
    tmsCursor.execute("update order_shipping_head set status = 1 where order_id = {0}".format(order_code))
    tmsConn.commit()
    if (tmsCursor.rowcount != 1):
        print "发货单状态回滚失败",
        tmsCursor.execute("select status from order_shipping_head where order_id = {0}".format(order_code))
        shipping_status = tmsCursor.fetchall()[0]['status']
        print "当前发货单状态为:" + str(shipping_status)
    else:
        print "发货单状态回滚完成"
except:
    print Exception, ":", e
    tmsConn.rollback()

#更改tms中签收单状态为"未到账",变更为1
try:
    tmsCursor.execute("update order_receipt_head set status = 1,pay_status = 1 where order_id = {0}".format(order_code))
    tmsConn.commit()
    if (tmsCursor.rowcount != 1):
        print "签收单状态回滚失败",
        tmsCursor.execute("select status from order_receipt_head where order_id = {0}".format(order_code))
        receipt_status = tmsCursor.fetchall()[0]['status']
        print "当前签收单状态为:" + str(receipt_status)
    else:
        print "签收单状态回滚完成"
except:
    print Exception, ":", e
    tmsConn.rollback()

#查询签收单号作为查询支付流水的trade_id
tmsCursor.execute("select receipt_order_id from order_receipt_head where order_id = {0}".format(order_code))
receipt_order_id = tmsCursor.fetchall()[0]['receipt_order_id']
#print receipt_order_id
tmsCursor.close()
tmsConn.close()

#更改payment中支付流水状态为"关闭",变更为6
paymentConn = MySQLdb.Connect(host='192.168.60.48', port=5201, user='root', passwd='root123', db='lsh_payment', charset="utf8")
paymentCursor = paymentConn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
try:
    paymentCursor.execute("update pay_deal set pay_status = 6 where trade_id = '{0}'".format(receipt_order_id))
    paymentConn.commit()
    if (paymentCursor.rowcount != 1):
        print "支付流水状态回滚失败",
        paymentCursor.execute("select pay_status from pay_deal where trade_id = '{0}'".format(receipt_order_id))
        pay_status = paymentCursor.fetchall()[0]['pay_status']
        print "当前支付流水状态为:" + str(pay_status)
    else:
        print "支付流水状态回滚完成"
except Exception,e:
    print Exception,":",e
    paymentConn.rollback()
paymentCursor.close()
paymentConn.close()