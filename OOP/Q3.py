class A:
    def __init__(self, x = 3):
        self._x = x

class B(A):
    def __init__(self):
        super().__init__()
    
    def display(self):
        print(self._x)

obj = B()
# obj = B(8) # this throws an error as __init__() of class B cannot get a parameter. Therefore A's __init__() will never get any other value than the default one i.e 3
obj.display()

# as '_x' means protected x, it was inherited by the child class, __x would not have been.