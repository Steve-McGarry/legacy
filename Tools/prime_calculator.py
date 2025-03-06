primes = []

for num in range(2,101):
    print(f'\nloop number {num}')
    prime = True
    for check in range(2, num):
        print(f'inner loop - check :{check}')
        if (num % check) == 0:
            prime = False
            break
        
    if prime:
        print(f'{num} is Prime')
        primes.append(num)

print(f'\nTotal number of prime numbers are {len(primes)}')
print(primes)