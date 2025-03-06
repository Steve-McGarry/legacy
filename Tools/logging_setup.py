import logging
import datetime

# for testing only
import time

now = datetime.datetime.now()

# day/month/hour/min/sec
suffix = now.strftime('%d%m%H%M%S')
# print(suffix)

# full path if needed, else log in same script as executed from
# path = '/Users/mcshine/Downloads/'
# file = f'example_{suffix}.log'
# log_file = path + file

log_file = f'example_{suffix}.log'
# print(log_file)

logging.basicConfig(filename=log_file,level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
logging.debug('This message should not go to the log file')
logging.info('This should as #1')

# insert sleep of 5 secs to offset timestamp
time.sleep(5)
logging.error('And this as #2')

