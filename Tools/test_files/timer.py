import timeit

# >>>Easy way
# import time
# start = time.time()
# print(start)

# for i in range(1000):
#     True
# time.sleep(2)

# end = time.time()
# print(end)

# elapsed = end - start
# print(f'Elapsed {elapsed:.5f}')

# fizzbuzz timer template

setup = 'f_counter, b_counter, fb_counter  = 0, 0, 0'

code = '''
for i in range(1,100):
    # print(f'processing the number "{i}"')
    x_three = 'Yes' if i%3 == 0 else 'No'
    x_five = 'Yes' if i%5 == 0 else 'No'
    if x_three and x_five == 'Yes':
        # print('FizzBuzz !')
        fb_counter += 1
    elif x_three == 'Yes':
        # print('Fizz !')
        f_counter += 1
    else:
        # print('Buzz !')
        b_counter += 1

print('fb count is ' + str(fb_counter))
print('f count is ' + str(f_counter))
print('b count is ' + str(b_counter))
'''
single = timeit.timeit(stmt=code, setup=setup, number = 1)
ten = timeit.timeit(stmt=code, setup=setup, number = 10)

print(f'Time for 1 iteration is: {single}')
print(f'Time for 10 iterations is: {ten}')