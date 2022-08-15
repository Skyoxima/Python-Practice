class MyClass():
    number = 12345
    string = "This is a class attribute, common for all the objects of this class" # these are still accessed through 'self' i.e object 

    def __init__(self, var1, var2):
        self.var1 = var1
        self.var2 = var2   # these are instance attributes, instance is analogous to an object of the class and these attributes are tied to self, which can be different for different self (objects)

    def func1(self):       # functions are class attributes too 
        print(f"{self.number}, {self.string}, {self.var1}, {self.var2}")

class MyClass2(MyClass): # by default inherits both attributes of the parent class but if has it's own __init__ then it only inherits class attributes, super().__init__ would be required for instance attributes
    pass


obj1 = MyClass(3, 7)
obj2 = MyClass(4, 8)
obj3 = MyClass2(5, 9)

print(dir(MyClass), "\n")  
print(dir(obj1), "\n")
print(dir(obj2), "\n")
print(dir(obj3), "\n")

# obj1.func1()
# obj2.func1()

#NOTE - in python classes, class attributes are attributes(variables & functions) which are common for all objects of that class and its children's objects too. These are usually outside the __init__() of the class
#NOTE - Instance attributes are attributes which are inside the __init__() function and are usually customizable for each object of that class (and its children's object)