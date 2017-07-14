# coding=utf-8
import sys
import MySQLdb
import json
import random
import requests
'''
obd push发货接口调用
运行时后面接订单号
'''
# for i in range(1, len(sys.argv)):
#     sequence = sys.argv[1]

sequence = 6285291416297938944
ofc = MySQLdb.connect(host='192.168.60.59', port=5200, user='root', passwd='', db='lsh_ofc', charset="utf8")
ofcCursor = ofc.cursor(cursorclass=MySQLdb.cursors.DictCursor)
sql = "select bill_details,out_order_id,system from ofc_bill where bill_type = 'ORDER' and order_id =" +str(sequence) +";"
ofcCursor.execute(sql)  
# list = ofcCursor.fetchall()[0]
data = ofcCursor.fetchall()
# print data

if data:
    for i in data:
        soCode = i["out_order_id"]
        obdCode = random.randint(1,1000000000000)
        waybillCode = random.randint(1,10000000)
        params = json.loads(i['bill_details'])['items']
        #print json.dumps(params)
        #print soCode
        zone_id = json.loads(i['bill_details'])['zone_id']
        list = []
        system = i['system']
        if system =='WUMART_SAP' and zone_id ==str(1000):
            DC = "DC42"
        elif system =='WUMART_SAP' and zone_id == str(2000):
            DC = 'DC42'
        elif system =='WUMART_SAP' and zone_id == str(1001):
            DC = 'DC40'
        elif system =='WUMART_SAP' and zone_id == str(1002):
            DC = 'DC59'
        elif system =='WUMART_SAP_JISHOU' and zone_id == str(1000):
            DC = 'DC42'
        elif system =='WUMART_SAP_JISHOU' and zone_id == str(2000):
            DC = 'DC42'
        elif system =='WUMART_SAP_JISHOU' and zone_id == str(1001):
            DC = 'DC40'
        elif system =='WUMART_SAP_JISHOU' and zone_id == str(1002):
            DC = 'DC59'
        for j in params:
            j['supplySkuCode']=j['sku_id']
            j['skuQty']=float(j['qty'])
            j['packNum'] = 4
            j['boxNum'] = 1
            j['leftEaNum'] = 0
            j['so_code'] = soCode
            if system == 'WUMART_SAP':
                j['supplier_org']=1
            elif system =='WUMART_SAP_JISHOU':
                j['supplier_org']=2
            #if j['obd']:
            list.append(j)
        data ={
        "wms": 1,
        "warehouseCode":DC,
        "soCode": soCode,
        "obdCode": obdCode,
        "waybillCode": waybillCode,
        "boxNum": 1,
        "turnoverBoxNum": 0,
        "driverInfo": "京QW71F2/李航凡/18332059010",
        "vehicleType": "TM02",
        "vehicleTypeDesc": "美批2吨",
        "createTime": "20160722",
        "pickTime": "20160722",
        "deliveryTime": "20160723",
        "carrierCode":"aaa",
        "carrierName":"lsh",
        "details": list
               }
        header = {'Content-Type':'application/json','api-version':'v1.0','random':1,'platform':1}
        host = 'http://test.api.ofc.lsh123.com'
        data = json.dumps(data)
        print data
        url = '/ofc/api/obd/push'
        url =  host + url
        response = requests.post(url,data=data,headers = header)
        print json.dumps(response.json())
else:
    print "订单没有提交到OFC请检查"

