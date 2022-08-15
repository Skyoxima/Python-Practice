class Test():
    def __init__(self):
        self.x = 0

class Derived_Test(Test):
    def __init__(self):
        super().__init__()
        self.y = 1


b = Derived_Test()
print(b.x, b.y)

# Output - Error as class Derived Test has it's own __init__ which overrides Test class's init, thereby making class Derived_Test not have variable x.
# Rectification - super().__init__() in Derived_Test class's __init__()