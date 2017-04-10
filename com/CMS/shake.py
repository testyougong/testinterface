# -*- coding: utf-8 -*-
import json

import requests
import sys
import MySQLdb
import time

reload(sys)
sys.setdefaultencoding('utf8')

a=0
b=0
c=0
d=0
e=0
users = 1000
activity_id = 110

'''
db = MySQLdb.connect(host='192.168.60.59', port=5200, user='root', passwd='', db='lsh_prizes', charset="utf8")
cursor = db.cursor(cursorclass=MySQLdb.cursors.DictCursor)
try:
    cursor.execute("delete from prize_record where activity_id = {0}".format(activity_id))
    db.commit()
except Exception,e:
    print Exception, ":", e
    db.rollback()
db.close()
'''
conn = MySQLdb.connect(host='192.168.60.59', port=5200, user='root', passwd='', db='lsh_market_dev', charset="utf8")
cursor = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
cursor.execute("select uid from user_info where zone_id = 1001 and status = 1 limit {0}".format(users))
data = cursor.fetchall()
conn.close()

for i in data:
    #print i['uid']
    uid = i['uid']
    items = []
    index = 0
    print uid,
    for j in range(0,3):
        host = 'http://qa2.market-h5.wmdev2.lsh123.com/re-cms-market/shake/play?activity_id='+str(activity_id)+'&uid='+str(uid)
        #params = {'activity_id': 1113,'uid':str(uid)}
        try:
            result = requests.get(host)
            #time.sleep(2)
            #print result.text
            if (str(result.json()['content']['got']) == '1'.decode('UTF-8')) :
                if (str(result.json()['content']['item'])=='1'.decode('UTF-8')):
                    b+=1
                    item = 1
                    items.append(item)
                    index += 1
                elif (str(result.json()['content']['item']) == '10'.decode('UTF-8')):
                    c += 1
                    item = 10
                    items.append(item)
                    index += 1
                elif (str(result.json()['content']['item']) == '20'.decode('UTF-8')):
                    d += 1
                    item = 20
                    items.append(item)
                    index += 1
                elif (str(result.json()['content']['item']) == '100'.decode('UTF-8')):
                    e += 1
                    item = 100
                    items.append(item)
                    index += 1
            elif (str(result.json()['content']['got']) == '2'.decode('UTF-8')):
                a += 1
                item = str(result.json()['content']['item'])
                items.append(item)
                index += 1
            elif (str(result.json()['content']['got']) == '3'.decode('UTF-8')):
                a +=1
                item = str(result.json()['content']['msg'])
                #print result.text
                items.append(item)
                index += 1
            else:
                print "抽奖异常"
                break

            if (index < 3):
                #print result.text
                print str(items[j]),
        except Exception, e:
            print Exception, ":", e
            print result.text

    if items[0] == 0 and items[1] == 0 and items[2] == 0:
        print str(items[2])+" "+"三次抽奖都没中奖"
    #elif (items[0]>1 and items[1]>1) or (items[0]>1 and items[2]>1) or (items[1]>1 and items[2]>1) :
        #print str(items[2])+" "+"至少抽中了两次大奖"
    else:
        print str(items[2])

print "不中奖:%d"%a,"概率为:%.2f"%((a/float(users*3))*100)+"%","默认概率:63%"
print "1块钱:%d"%b,"概率为:%.2f"%((b/float(users*3))*100)+"%","默认概率:30%"
print "10块钱:%d"%c,"概率为:%.2f"%((c/float(users*3))*100)+"%","默认概率:6%"
print "20块钱:%d"%d,"概率为:%.2f"%((d/float(users*3))*100)+"%","默认概率:0.9%"
print "100块钱:%d"%e,"概率为:%.2f"%((e/float(users*3))*100)+"%","默认概率:0.1%"