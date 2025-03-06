from datetime import datetime
import time
from contextlib import redirect_stdout
import os
# src = '1gtest'
# dst = ':/home/ubuntu/tesfile'
count = 1
log = 'output_premium_500.txt'
for i in range(50):
    print(f'Starting new loop {count}')
    now = datetime.now()
    with open(log, 'a') as file:
        with redirect_stdout(file):
            # os.system ('scp me.txt /tmp')
            os.system('scp -i "sing.pem" 500mtest ubuntu@ec2-52-221-230-138.ap-southeast-1.compute.amazonaws.com:/home/ubuntu/testfile')
    end = datetime.now()
    run = end - now
    count += 1
    with open(log, 'a') as file:
        file.write(f'run time loop {count} was {run}\n')
