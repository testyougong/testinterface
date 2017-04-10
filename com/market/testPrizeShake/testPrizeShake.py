# -*- coding: utf-8 -*-
import requests
import json
import MySQLdb
import xlrd

list = []
amountTrue = 0
conn = MySQLdb.connect(host='192.168.60.59', port=5200, user='root', passwd='', db='lsh_market_dev', charset="utf8")
cursor = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
#excel = xlrd.open_workbook('/Users/zhouxin/PycharmProjects/testinterface/query_result2.xls',encoding_override="utf-8")
#sheet = excel.sheets()[0]
#nrows = sheet.nrows

for k in range(0,3):
    # 使用excel取uid
    # for i in range(1, nrows):
    # host='http://qa.market-api.wmdev2.lsh123.com'
    # excel_uid = sheet.cell(i,0).value
    # uid = excel_uid.replace(',', '')
    #获取用户的数量
    cursor.execute("select count(*) from user_info where zone_id = 1001 and status = 1 order by created_at ASC")
    count = cursor.fetchall()
    #count_person = int(count[0]['count(*)'])
    #获取uid
    cursor.execute("select uid from user_info where zone_id = 1001 and status = 1 limit 500")
    uid_sql = cursor.fetchall()
    activity_id = raw_input("请输入活动id:")
    for m in range(0, 500):
        uid = int(uid_sql[m]['uid'])
        print uid
        host = 'http://qa.market-api.wmdev2.lsh123.com'
        params = {'uid' : str(uid) ,'activity_id' : activity_id}
        result = requests.post( host +'/Operate/prize/shake' ,params = params)
        #print json.dumps(result.json())
        ResponseTime = (result.elapsed.microseconds) / 1000
        print "shake接口响应时间:" + str(ResponseTime) + "ms"
        time = list.append(ResponseTime)
        try:
            if (str(result.json()['content']['got']) == 'True'):
                print "中奖啦"
                print json.dumps(result.json())
                '''
                timestamp = result.json()['timestamp']
                sql = "select count(*) from prize_draw_record where got = 1 and time = '{0}'".format(timestamp)
                cursor.execute(sql)
                data = cursor.fetchall()
                #print int(data[0]['count(*)'])
                if (int(data[0]['count(*)']) == 1):
                    print "抽奖记录正常写入数据库"
                else:
                    print "抽奖记录没有写入数据库"
                '''
                sql = "select b.coupon_value from user_coupon as a left join coupon_info as b on a.coupon_id = b.coupon_id where uid = '{0}' order by a.created_at DESC limit 1".format(uid)
                cursor.execute(sql)
                data = cursor.fetchall()
                coupon_value = int(data[0]['coupon_value'])
                prize = result.json()['content']['prize']
                item = int(eval(json.dumps(prize))['item'])
                if(item == coupon_value):
                    print "优惠券下发pass"
                else:
                    print "优惠券下发failure"
                amountTrue += 1
        except Exception, e:
            print Exception, ":", e
            print result.text

total = 0
for j in list:
    total+=j

avg = total/len(list)
probability = amountTrue/float(1500)
print "shake接口平均响应时间:" + str(avg) +'ms'
print "中奖概率:%.2f" %(probability)