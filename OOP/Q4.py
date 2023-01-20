#this is exception handling, not object oriented
def procedural(val1):
    try:
        sum1 = 0
        for item in str(val1):
            sum1 += int(item_val)
    except TypeError:
        print("Type error has occurred")
    finally:
        print("Finally inside the function")
    print("Function executed successfully")

try:
    procedural(792)
    print("Try handled") # skipped, as soon as an error occurs the rest of the try block is skipped
except ValueError:
    print("Value error occurred")
except NameError:
    print("Name error occurred")
finally:
    print("Finally in main")

# if inner try doesn't have a satisying except then outer try ka except is used, so try - except - finally inner then except outside then finally outside