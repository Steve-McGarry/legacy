from datetime import datetime, timedelta

now = datetime.now()
print(now)
ts = now.timestamp()
print(type(ts))
print(ts)
ts_temp = str(ts)[:-7]
print(type(ts_temp))
print(ts_temp)
ts_short = int(ts_temp)
print(type(ts_short))
print(ts_short)
fmt = now.strftime('%Y-%m-%dT%H:%M:%SZ')
print(fmt)

import time 
    
# Get the epoch 
obj = time.gmtime(0) 
epoch = time.asctime(obj) 
print("epoch is:", epoch) 
    
# Get the time in seconds 
# since the epoch 
# using time.time() method
time_sec = time.time() 
  
# Get the time in nanoseconds
# since the epoch
# using time.time_ns() method
time_nanosec = time.time_ns()
    
# Print the time 
# in seconds since the epoch 
print("Time in seconds since the epoch:", time_sec) 
  
# Print the time 
# in nanoseconds since the epoch 
print("Time in nanoseconds since the epoch:", time_nanosec)