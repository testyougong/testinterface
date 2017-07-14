# -*- coding: UTF-8 -*-

import threading
import time
import MySQLdb
import requests

exitFlag = 0
timeList = []


class myThread(threading.Thread):  # 继承父类threading.Thread
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter

    def run(self):  # 把要执行的代码写到run函数里面 线程在创建后会直接运行run函数
        print "Starting " + self.name
        order(self.name, self.counter, 1)
        print "Exiting " + self.name


def order(threadName, delay, counter):
    while counter:
        if exitFlag:
            threading.Thread.exit()
        time.sleep(delay)
        host = 'http://qa.market-mis.wmdev2.lsh123.com'
        headers = {'Cookie1': 'MISSESSID=vgia9bgicv5k84fdrcqi1h10l5; zone_id=1002'}
        conn = MySQLdb.Connect(host='192.168.60.59', port=5200, user='root', passwd='', db='lsh_market_dev',charset="utf8")
        cursor = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        cursor.execute("select A.uid , B.address_id from user_info as A left join user_address as B on A.uid = B.uid where A.zone_id = 1002 and B.status = 3 and B.is_default = 1 limit 2")
        data = cursor.fetchall()
        for row in data:
            uid = row['uid']
            addressId = row['address_id']
            zone_id = 1002
            skuList = '[{"sku_id":"120639","qty":"1","selected":"1"}]'
            params = {'uid': uid, 'sku_list': skuList, 'address_id': addressId, 'coupon_id': '', 'invoice_type': 2,
                      'zone_id': zone_id}
            try:
                result = requests.post(host + '/order/ka/init', params=params, headers=headers)
                responseTime = (result.elapsed.microseconds)/1000
                timeList.append(responseTime)
                print responseTime
                if len(timeList) > 1 :
                    if timeList[len(timeList)-1] < timeList[len(timeList)-2] :
                        temp = timeList[len(timeList)-2]
                        timeList[len(timeList)-2] = timeList[len(timeList)-1]
                        timeList[len(timeList)-1] = temp
                if result.json()['ret'] != 0 :
                    print result.text
            except Exception, e:
                print e
        print "%s: %s" % (threadName, time.ctime(time.time()))
        counter -= 1
    averageTime = sum(timeList)/len(timeList)
    minTime = timeList[0]
    maxTime = timeList[len(timeList)-1]
    print "平均响应时间:%d"%averageTime
    print "最小响应时间:%d"%minTime
    print "最大响应时间:%d"%maxTime

# 创建新线程
for thread in range(1,3):
    print "Thread-"+str(thread)
    t = myThread(thread,"Thread-"+str(thread),thread)
    #thread1 = myThread(1, "Thread-1", 1)
    #thread2 = myThread(2, "Thread-2", 2)

# 开启线程
    t.start()
#thread1.start()
#thread2.start()

print "Exiting Main Thread"