# -*- coding: utf-8 -*-

items = []
item = '123'
item2 = 'xxxxx'
item3 = '123'
items.append(item)
items.append(item2)
items.append(item3)
print items

set = set()
id = '123'
id2 = 'xxxxx'
id3 = '123'
set.add(id)
set.add(id2)
set.add(id3)
print set
ids = ""
for row in set :
    ids += row
    ids += ","
print ids[0:-1]

a = '4'
if a:
    print '123'
else :
    print '456'

a = 9999
b = 8888
data = {"1234":"4321","4567":"7654"}
data[str(a)] = str(b)
print data
print len(data)
for i in range(0,len(data)):
    print data.keys()[i],":",data[data.keys()[i]]