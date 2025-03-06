import os
import time
import subprocess
from contextlib import redirect_stdout
from datetime import datetime

hosts_d = {'lon_p': 'London', 'la_p': 'LA', 'hk_p': 'Hong Kong'}
# hosts_d = {'ubuntu-focal-1': 'London', 'ubuntu-focal-2': 'LA', 'ubuntu-focal-3': 'Hong Kong'}
hosts = list(hosts_d.keys())
hostname = os.uname()[1]
targets = []
loops = 3

file_path = ':/DATA/'
src = '10mtest'

# setup log file
now = datetime.now()
time_stamp = now.strftime('%d%m_%H%M')
log_file = f'results_public-{time_stamp}.txt'

# create list of hosts to check
if hostname == hosts[0]:
    # print(hosts[0])
    targets = [hosts[1], hosts[2]]
elif hostname == hosts[1]:
    # print(hosts[1])
    targets= [hosts[0], hosts[2]]
else:
    # print(hosts[2])
    targets = [hosts[0], hosts[1]]

runtime = []
count = 1

def average(num_list):
    return sum(num_list) / len(num_list)

# tidy up before next run
if os.access(log_file, os.F_OK):
    print('Deleted stale log file')
    os.system(f'rm {log_file}')
else:
    print('No old log files found.')

# main loop
for t in targets:
    os.system('clear')
    dst = t + file_path
    print(f'#### Testing connectivity to {hosts_d[t]}')
    for i in range(loops):
        os.system(f'ssh {t} rm -rf /DATA/*')
        start = time.time()
        print(f'>>>> Starting Loop {count} <<<<')
        os.system(f'rsync -hvP {src} {dst}')
        print('\n')
        stop = time.time()
        duration_raw = stop - start
        duration = f'{duration_raw:.3f}'
        runtime.append(float(duration))
        count += 1

    avg = average(runtime)

    print('>>>> Starting ping test... <<<<\n\n')
    response_string = subprocess.check_output(['ping', '-c', '5', t],
    stderr=subprocess.STDOUT, universal_newlines=True)

    new_substring = response_string.partition('rtt ')

    with open(log_file, 'a') as file:
        with redirect_stdout(file):
            print(f'* * * * *   RESULTS : {hosts_d[hostname]} to {hosts_d[t]}    * * * * *\n')
            print(f'Average transfer time for {runtime} is:', round(avg, 2), '\n')
            print('Ping statistics for 5 packets:', new_substring[2])

    print(f'* * * * *   RESULTS : {hosts_d[hostname]} to {hosts_d[t]}    * * * * *\n')
    print(f'Average transfer time for {runtime} is:', round(avg, 2), '\n')
    print('Ping statistics for 5 packets:', new_substring[2])

    # reset for next site iteration
    runtime = []
    count = 1

# present the results
os.system('clear')
# print('\n\n\n\n\n')

with open(log_file) as f:
    print(f.read())