# -*- coding: utf-8 -*-

list1 = ["a","b","c"]
list2 = ["1","2","3"]
d = zip(list1, list2)
print d
d = dict(d)
print d
for  key, value in d.items():
    print  key, value