import calendar
from datetime import datetime

interval = 3600 # hour in seconds
year = 2023
months_dict = {'Jan':1, 'Feb':2, 'March':3, 'April':4, 'May':5, 'June':6, 'July':7, 'Aug': 8, 'Sep':9, 'Oct':10, 'Nov': 11, 'Dec':12}
query_month = 'July' # update as per months_dict keys

# check num days in months
month_days_dict = {}
for month in months_dict:
    # print(month)
    # print(months_dict[month])
    # print(calendar.monthrange(year, months_dict[month])[1])
    days = calendar.monthrange(year, months_dict[month])[1]
    month_days_dict[month] = days

print(month_days_dict)

# calc epoch steps for API call
# total_days = month_days_dict[query_month]
total_days = 31
total_hours = total_days * 24
print(total_days,total_hours)

format_string = "%d-%m-%Y %H:%M:%S"
start_day = 1
month = months_dict[query_month]
stop_day = 1
# stop_day = month_days_dict[query_month]
start_hour = 00
start_minute = 00
start_second = 00
stop_hour = 23
stop_minute = 59
stop_second = 59
# EXAMPLE start_date_string = '"31-1-2020 14:45:37"'
start_date_string = f'{start_day}-{month}-{year} {start_hour}:{start_minute}:{start_second}'
start_date = datetime.strptime(start_date_string, format_string)
epoch_start = str(start_date.timestamp())[:-2]
stop_date_string = f'{stop_day}-{month}-{year} {stop_hour}:{stop_minute}:{stop_second}'
stop_date = datetime.strptime(stop_date_string, format_string)
epoch_stop = str(stop_date.timestamp())[:-2]

print(start_date,epoch_start,f'\n{stop_date}',epoch_stop)

start_epoch = 1691967600
stop_epoch = 1692054000

# check epoch to world time
print("The epoch is:")
print(start_epoch,stop_epoch)
datetime_obj_s=datetime.fromtimestamp(start_epoch)
datetime_obj_e=datetime.fromtimestamp(stop_epoch)
print("The datetime objects are:")
print(datetime_obj_s,datetime_obj_e)

# 8888888888888888 testing
epoch_list = []
print(epoch_list)
count = 1
while start_epoch < stop_epoch:
    print(f'current: {start_epoch}')
    temp_start = start_epoch
    start_epoch += 3600
    epoch_list.append((temp_start,start_epoch))
    print(f'hours={count}')
    count += 1
else:
    print(f'difference = {stop_epoch-start_epoch}')
    print(f'\nTarget reached :{start_epoch}')

print(epoch_list)
print(len(epoch_list))
