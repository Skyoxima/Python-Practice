class A:
    def test(self):
        print("\n'test' of  A  called\n")

class B(A):
    def test(self):
        print("\n'test' of  B  called")
        super().test()       #? Why does this ask it to continue looking for test -- check detailed

class C(A):
    def test(self):
        print("\n'test' of  C  called")
        super().test()

class D(B, C):              # MRO - Method Resolution Order - Multiple Inheritance ~ Left to Right fashion    
    def test2(self):
        print("\n'test' of  D  called")
    # class D doesn't have the test function so parent classes will be checked

obj = D()
obj.test()
print(D.__mro__)

#NOTE - The super() function returns a temporary object of the superclass that allows access to all of its methods to its child class.
#NOTE - When accessing methods of parent class using the name of the parent class, you have to pass the 'self' to that method, whereas doing the same
# with super() does not require you to pass 'self'

#? - Why is the order D -> B -> C -> A
# NOTE --> the super().test() in parent classes allow the MRO to move forward, MRO of the class whose object is instantiated otherwise the execution will stop at the first found match of the called function
# which here is test of class B

#Check the Q5detailed.py for more info on this