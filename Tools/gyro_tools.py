# import requests
import json
import os
import sys
import calendar
# from datetime import datetime

url = ''
headers = ''

def auth_template():
    # auth_file = input('Please enter full path to Auth file: ')
    auth_file = '/Users/stevemcgarry/Downloads/MCSHINE/access_testing.json'

    with open(auth_file) as file:
        data = json.load(file)

    os.system('clear')
    # EMAIL = input('\n>>> Please enter username to authenticate with: ')
    # print(EMAIL)
    EMAIL = 'steve.mcgarry@kerv.com'

    for user in data['users']:
        if user['userId'] == EMAIL:
            PASSWD = user['passwd']
    
    return EMAIL, PASSWD

def api_template(*args):
    # auth_file = input('Please enter full path to API file: ')
    api_file = '/Users/stevemcgarry/Downloads/MCSHINE/api_keys.json'
    
    with open(api_file) as file:
            data = json.load(file)

    def lookup(api_name):
        for provider in data['keys']:
            if provider['target'] == api_name:
                ans = provider['key']
        
        return ans

    result = len(args)

    if result > 0:
        api_name = args[0]
        key = lookup(api_name)
    else:
        os.system('clear')
        api_name = input('\n>>> Please enter API provider name to authenticate with: ')
        key = lookup(api_name)
    
    return key

def jprint(obj):
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

def test_func ():
    print('\nImport working OK from Gyro_Utility.py updated')

def clrscr():
    # Check if Operating System is Mac and Linux or Windows
    if os.name == 'posix':
        _ = os.system('clear')
    else:
        # Else Operating System is Windows (os.name = nt)
        _ = os.system('cls')

def json_check():
    # if status code of api call is tex.html will get json import error
    # the following code lists content type
    h = requests.head(url, headers=headers)
    header = h.headers
    contentType = header.get('content-type')
    print(contentType)

def readable_size(wtx, decimal_point=3):
    for i in ['B', 'KB', 'MB', 'GB', 'TB']:
        if wtx < 1024.0:
            break
        wtx /= 1024.0
    
    return f"{wtx:.{decimal_point}f}{i}"

def epoch_range_ts(start, stop, interval=3600):
    # takes EPOCH start/stop
    # Total number of hours/days between to dates in seconds, and generates list of epoch timestamps at given interval
    # output to screen first/last & list of all start/stop tuple pairs
    epoch_list = []
    count = 1
    start_epoch = start
    stop_epoch = stop
    # start_epoch = sys.argv[1]
    # stop_epoch = sys.argv[2]
    while start_epoch < stop_epoch:
        # print(f'current: {start_epoch}')
        temp_start = start_epoch
        start_epoch += interval
        epoch_list.append((temp_start,start_epoch))
        count += 1
    else:
        print(f'difference = {stop_epoch-start_epoch}')
        # print(f'\nTarget reached :{start_epoch}')

    length = len(epoch_list)
    days = length/24
    print(f'Total hours / Days : {length} / {days}')

    new_count = 1
    last = (length - 5)
    print('First 5')
    for i in epoch_list:
        if new_count <= 5:
            print(i)
            new_count+= 1
        elif new_count < last:
            new_count += 1 
        elif new_count == last:
            print('\nLast 5')
            print(i)
            new_count+= 1
        elif new_count > last:
            print(i)
            new_count+= 1
        else:     
            print('Processing complete')
        
    return epoch_list

def epoch_range_td(start, stop, interval=3600):
    # takes timedate object start/stop; EXAMPLE string = '"31-1-2020 14:45:37"
    # Total number of hours/days between to dates in seconds, and generates list of epoch timestamps at given interval
    # output to screen first/last & list of all start/stop tuple pairs
    format_string = "%d-%m-%Y %H:%M:%S"
    start_date_string = start
    start_date = datetime.strptime(start_date_string, format_string)
    start = str(start_date.timestamp())[:-2]
    start_epoch = int(start)
    stop_date_string = stop
    stop_date = datetime.strptime(stop_date_string, format_string)
    stop = str(stop_date.timestamp())[:-2]
    stop_epoch = int(stop)
    print(start_epoch,stop_epoch)

    epoch_list = []
    count = 1
    # start_epoch = sys.argv[1]
    # stop_epoch = sys.argv[2]
    while start_epoch < stop_epoch:
        # print(f'current: {start_epoch}')
        temp_start = start_epoch
        start_epoch += interval
        epoch_list.append((temp_start,start_epoch))
        count += 1
    else:
        print(f'difference = {stop_epoch-start_epoch}')
        # print(f'\nTarget reached :{start_epoch}')

    length = len(epoch_list)
    days = length/24
    print(f'Total hours / Days : {length} / {days}')

    new_count = 1
    last = (length - 3) + 1
    # print(last)
    print('First 3')
    for i in epoch_list:
        if new_count <= 3:
            print(i)
            new_count+= 1
        elif new_count < last:
            new_count += 1 
        elif new_count == last:
            print('\nLast 3')
            print(i)
            new_count+= 1
        elif new_count > last:
            print(i)
            new_count+= 1
        else:     
            print('Processing complete')
        
    return epoch_list, start_date, stop_date

def epoch_endstops(start=1,stop=2, month='July', year=2023, interval=3600):
    # produce and verify start and ent epoch times
    # interval = 3600 # hour in seconds
    months_dict = {'Jan':1, 'Feb':2, 'March':3, 'April':4, 'May':5, 'June':6, 'July':7, 'Aug': 8, 'Sep':9, 'Oct':10, 'Nov': 11, 'Dec':12}
    # query_month = 'July' # update as per months_dict keys
    query_month = month
    
    # check num days in months
    month_days_dict = {}
    for month in months_dict:
        days = calendar.monthrange(year, months_dict[month])[1]
        month_days_dict[month] = days

    format_string = "%d-%m-%Y %H:%M:%S"
    start_day = start
    month = months_dict[query_month]
    stop_day = stop
    # stop_day = month_days_dict[query_month]
    start_hour = 00
    start_minute = 00
    start_second = 00
    stop_hour = 00
    stop_minute = 00
    stop_second = 00
    stop_hour_EoD = 23
    stop_minute_EoD = 59
    stop_second_EoD = 59
    # EXAMPLE start_date_string = '"31-1-2020 14:45:37"'
    start_date_string = f'{start_day}-{month}-{year} {start_hour}:{start_minute}:{start_second}'
    start_date = datetime.strptime(start_date_string, format_string)
    epoch_start = str(start_date.timestamp())[:-2]
    stop_date_string = f'{stop_day}-{month}-{year} {stop_hour}:{stop_minute}:{stop_second}'
    stop_date = datetime.strptime(stop_date_string, format_string)
    epoch_stop = str(stop_date.timestamp())[:-2]

    print(start_date,epoch_start,f'\n{stop_date}',epoch_stop)

def seconds_summary(seconds):

    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    
    return "%d:%02d:%02d" % (hour, minutes, seconds)

def replace_line(filename, search_term, replace_text):
  """
  Opens a file, searches for a line containing the search term, and replaces it with the replace text.

  Args:
      filename (str): The name of the file to modify.
      search_term (str): The word or phrase to search for in the file.
      replace_text (str): The text to replace the line with if the search term is found.
  """
# Example usage: Replace line with "string" with "new line" in "my_file.txt"
# replace_line("my_file.txt", "search string", "new line")
  
  # Read the file contents into a list of lines
  with open(filename, "r") as f:
    lines = f.readlines()

  # Flag to track if a replacement was made
  replaced = False

  # Loop through lines, search, and replace
  for i, line in enumerate(lines):
    if search_term in line:
      lines[i] = replace_text  # Replace the line
      replaced = True
      break  # Exit the loop after the first replacement

  # Write the modified lines back to the file
  if replaced:
    with open(filename, "w") as f:
      f.writelines(lines)
    print(f"Replaced line containing '{search_term}' in '{filename}'.")
  else:
    print(f"No line containing '{search_term}' found in '{filename}'.")