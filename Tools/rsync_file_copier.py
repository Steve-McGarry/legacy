import os
import time
import subprocess

hosts = ['ubuntu-focal-1', 'ubuntu-focal-2', 'ubuntu-focal-3']
hostname = os.uname()[1]
targets = []

src = '/Users/smcgarry/Downloads/Projects/VS_Python/Tools/test_files/file.pdf'
# dst = '/Users/smcgarry/Downloads/Projects/VS_Python/Tools/test_files/TEMP_OUT/'

file_path = '/Users/smcgarry/Downloads/Projects/VS_Python/Tools/test_files/TEMP_OUT/'
# file_path = '/DATA/'
test_file = '1gtest'
# src = file_path + test_file

if hostname == hosts[0]:
    print(hosts[0])
    targets = [hosts[1], hosts[2]]
elif hostname == hosts[1]:
    print(hosts[1])
    targets= [hosts[0], hosts[2]]
else:
    print(hosts[2])
    targets = [hosts[0], hosts[1]]

print(targets)

runtime = []
loops = 2
count = 1

def average(num_list):
    return sum(num_list) / len(num_list)

os.system('clear')

for t in targets:
    print(hostname)
    for i in range(loops):
        start = time.time()
        print(f'>>>> Starting Loop {count} <<<<\n')
        # os.system(f'rsync -hvP --stats {src} {dst}')
        os.system(f'rsync -hvP {src} {file_path}')
        print('\n')
        stop = time.time()
        duration_raw = stop - start
        duration = f'{duration_raw:.3f}'
        runtime.append(float(duration))
        count += 1

    avg = average(runtime)

    print('>>>> Starting ping test... <<<<\n\n')
    response_string = subprocess.check_output(['ping', '-c', '5', '8.8.8.8'],
    stderr=subprocess.STDOUT, universal_newlines=True)

    new_substring = response_string.partition('round-trip ')

    print(f'* * * * *   RESULTS : {hostname} to {t}    * * * * *\n')
    print(f'Average transfer time for {runtime} is:', round(avg, 2), '\n')
    print('Ping statistics for 5 packets:', new_substring[2])