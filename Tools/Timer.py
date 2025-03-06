# multiple ways to time script
# easy
# import time
# start = time.time()
# >>> do stuff
# end = time.time()
# duration = end - start 

# longer
import timeit

mysetup = "from math import sqrt"

mycode = '''
def example():
    mylist = []
    for x in range(100):
        mylist.append(sqrt(x))
'''
print(timeit.timeit(setup=mysetup, stmt=mycode, number=10000))