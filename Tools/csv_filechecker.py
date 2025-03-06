import csv
import sys

sys.path.append ('/home/ubuntu/Projects/Velocloud/Tools')
from gyro_tools import *

#src_file = '/Users/stevemcgarry/Projects/VS_Python/VCE/v1/input/sutton.csv'
src_file = input('Enter CSV input filename: ')

clrscr()
print('* * * Start of CSV verification * * *')
# parse by line
with open(src_file) as input_strings:
    print('\n> Checking headers...')
    reader = csv.reader(input_strings)
    line_count = 0

    for row_s in reader:
        if line_count == 0:
            headings = []
            for i in row_s:
                headings.append(i)
            print(headings)
            print(f'\nThere are {len(headings)} headers identified.')
            line_count += 1
        else:
            line_count += 1

    print(f'\nTotal number of rows are {line_count -1}')

# parse as dict - ignores headers
with open(src_file) as input_dict:
    print('\n> Checking Dictionary')
    reader2 = csv.DictReader(input_dict)
    row_count = 1
    data_rows = line_count -1

    for row_d in reader2:
        if row_count == 1:
            print(f'\nFirst line of file:')
            print(f'name: {row_d["SD-WAN Appliance Hostname"]}')
            row_count += 1
        elif row_count == data_rows:
            print('\nLast line of file:')
            print(f'name: {row_d["SD-WAN Appliance Hostname"]}')
        else:
            row_count += 1

    print(f'\nProcessed dictionary {row_count} entries - completed EOF')