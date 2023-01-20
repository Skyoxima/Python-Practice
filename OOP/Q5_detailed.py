class A:
    def test(self):
        print("Entered 'test' of  class A")
        print("Exited 'test' of  class A")

class B(A):
    def test(self):
        print("Entered 'test' of  class B")
        super().test()      
        print("Exited 'test' of  class B")

class C(A):
    def test(self):
        print("Entered 'test' of  class C")
        super().test()      
        print("Exited 'test' of  class C")

class D(B, C):         
    def test(self):
        print("Entered 'test' of  class D")
        super().test()      
        print("Exited 'test' of  class D")

obj = D()  # object is of class D so its MRO will be followed
print("\n\033[38;5;225m", D.mro(), "\033[0m\n")
obj.test()

#* MRO is basically decided by this: check base class before parent class and no repeat checks for any class. Base class here is D
#! the super().test() calls/checks the next class according to the MRO used. NOT the MRO of the class it is called in (This was the main confusion) 
#! [maybe because under the hood super() always is getting the obj of class D (instantiated class)]

#! MRO is essentially used like this with super() ~ 'cooperative subclassing'
#* if parent class names were used then it is very straightforward what will be printed.