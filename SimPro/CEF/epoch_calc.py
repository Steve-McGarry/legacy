import datetime
import time

def get_epoch_start_end(year, month):
    # Create the start datetime for the first day of the given month
    start_date = datetime.datetime(year, month, 1)  # First day of the month
    
    # Create the end datetime for the last day of the given month
    # The last day is the first day of the next month minus one second
    if month == 12:  # If December, go to January of the next year
        end_date = datetime.datetime(year + 1, 1, 1) - datetime.timedelta(seconds=1)
    else:
        end_date = datetime.datetime(year, month + 1, 1) - datetime.timedelta(seconds=1)

    # Convert to epoch time (seconds since 1970-01-01)
    start_epoch = int(time.mktime(start_date.timetuple()))
    end_epoch = int(time.mktime(end_date.timetuple()))

    return start_date, start_epoch, end_date, end_epoch

# Example usage
year = 2023
month = 10  # October
start_date, start_epoch, end_date, end_epoch = get_epoch_start_end(year, month)

print(f"Start of {year}-{month}: {start_epoch} (epoch time)")
print(f"End of {year}-{month}: {end_epoch} (epoch time)")

print(f'start {start_date}')
print(f'end {end_date}')  # This will print the last day of the month