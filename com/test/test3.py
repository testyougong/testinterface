# -*- coding: UTF-8 -*-
import time
import calendar

var_1 = 10
del var_1

s = 'ilovepython'
print s[-1]
list = [ 'runoob', 786 , 2.23, 'john', 70.2 ]
list[2] = '123'
list.insert(3,'456')
print list
print list[1:3]

a = 10
b = 20

print (a and b)
if ( a and b ):
   print "1 - 变量 a 和 b 都为 true"
else:
   print "1 - 变量 a 和 b 有一个不为 true"
u'Hello World !'
print u'Hello World !'

dict = {'Name': 'Zara', 'Age': 7, 'Name': 'Manni'}
print str(dict)
print dict
print dict.values()
print dict.copy()
print dict.has_key('Name')
s = time.time()
ss = time.localtime(s)
print s
print ss
print time.asctime(ss)
print time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

cal = calendar.month(2017,1)
print cal