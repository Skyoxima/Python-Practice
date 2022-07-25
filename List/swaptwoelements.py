list1 = [int(i) for i in input("Enter the numbers for the list: ").split()]
psn = [int(i) for i in input("Enter the positions(indices) that are needed to be swapped: ").split()][:2]
print("Before interchanging: ", end = " "); print(*list1, sep = ', ')

#Pythonic Way
list1[psn[0]], list1[psn[1]] = list1[psn[1]], list1[psn[0]]
print("After interchanging: ", end = " "); print(*list1, sep = ', ')