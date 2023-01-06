class A:
    def __init__(self, a= 0, b= 3):
        self.a = a
        self.b = b
    def __repr__(self):
        return '{},{}'.format(self.a, self.b)

a = A(5, 3)
b = A(3, 7)
l =[a ,b]
l1 = sorted(l, key =lambda t: t.a)
print(l1)