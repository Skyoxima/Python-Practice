class A:
    def __init__(self):
        self.x = 1

    def __str__(self):
        return f'{self.x}'

class B(A):
    def __init__(self): # now this is not useless, as distinct variables (both in this one) are used in both classes for their __str__() functions
        super().__init__()
        self.y = 2
    
    def __str__(self):
        return f"({self.y} + {self.x})"
        
class C(B):
    def __init__(self):
        super().__init__()

obj1 = B()
obj2 = A()
obj3 = C()

print(obj1, obj2, obj3)