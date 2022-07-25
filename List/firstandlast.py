print("\033[38;5;207mPython program to interchange first and last elements of a list\033[0m")
list1 = [int(i) for i in input("Enter the numbers of the list: ").split()]
print("Before interchanging: ", end = " "); print(*list1, sep = ', ')

# First Pythonic way
list1[-1], list1[0] = list1[0], list1[-1]
print("After interchanging (Method 1): ", end = " "); print(*list1, sep = ', ')

# Second Pythonic way
first, *middle, last = list1
list1 = [last, *middle, first]
print("After interchanging (Method 2): ", end = " "); print(*list1, sep = ', ')

# there's always the basic temp variable swapping way
