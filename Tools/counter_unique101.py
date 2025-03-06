import pandas as pd
from random import randint
from collections import Counter

# generate list of random numbers
# rlist = []
# for i in range(20):
#     rlist.append(randint(1,10))

rlist = [7, 1, 6, 3, 5, 3, 5, 9, 8, 3, 3, 8, 6, 5, 2, 5, 5, 10, 9, 2]
print('New list')
print(rlist)

print('\ncount an item')
print(rlist.count(1))

print('\nlist comprehension for unique values')
print([x for x in set(rlist)])

print('\ncounter list using comprehension')
print([[x,rlist.count(x)] for x in set(rlist)])

print('\nfastest using dictionary')
def counter_dict():
    dict1 = {}
    for i in rlist:
        if i in dict1:
            dict1[i] += 1
        else:
            dict1[i] = 1
    print(dict1)

counter_dict()

print('\nusing counter from collections')
print(Counter(rlist))

print('\n also using pandas')
count = pd.Series(rlist).value_counts
print(count)