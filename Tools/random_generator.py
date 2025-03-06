import random
import time

random_list = []
for i in range(10):
    n = random.randint(20,30)
    random_list.append(n)

print('random list1 in list/loop')
print(random_list)

random_list2 = random.sample(range(20,30),10)

print('random list2 range')
print(random_list2)

print('random_list3 from loop')
for i in range(10):
    n = random.randint(20,30)
    print(n)
    time.sleep(0.5)