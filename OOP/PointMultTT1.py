# Topic is operator overloading

class Point():
    def __init__(self, x, y):
        self.x_cord = x
        self.y_cord = y

    def __str__(self):
        return f"X co-ordinate: {self.x_cord}, Y co-ordinate: {self.y_cord}" 
   
    def __mul__(self, other):
        self.new_x = self.x_cord * other.x_cord
        self.new_y = self.y_cord * other.y_cord
        return Point(self.new_x, self.new_y)  # returns a point object

P1 = Point(2, 3)
P2 = Point(4, 5)
P3 = P1 * P2    # equivalent to calling P1.__mul__(P2)
print(P3)

# + - __add__
# - - __sub__
# * - __mul__
# / - __truediv__