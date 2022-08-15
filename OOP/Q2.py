class A:
    def __str__(self):  # this does get inherited by the child class
        return "1"

class B(A):
    def __init__(self): # this is essentially useless as class A doesn't have any __init__, other functions of class A are inherited directly
        super().__init__()

    # def __str__(self):  # this will override the class A's __str__ and class C will also inherit this __str__
    #     return "2"     

class C(B):
    def __init__(self):
        super().__init__()

obj1 = B()
obj2 = A()
obj3 = C()

print(obj1, obj2, obj3)