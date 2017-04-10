# -*- coding: UTF-8 -*-

class Vector:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __str__(self):
        print 'Vector1 (%d, %d)' % (self.a, self.b)
        return 'Vector (%d, %d)' % (self.a, self.b)

    def __add__(self, other):
        print 'Vector2 (%d, %d)'%(other.a,other.b)
        return Vector(self.a + other.a, self.b + other.b)


v1 = Vector(2, 10)
v2 = Vector(5, -2)
print v1 + v2

