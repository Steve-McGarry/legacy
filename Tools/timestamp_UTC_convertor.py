import requests
import json
from datetime import datetime

key = 'VPNZCHQPMNHI'
src_timezone = 'Africa/Banjul'
dst_timezone = 'Europe/London'
timestamp = 1634019720

# UTC > London default
api = f'http://api.timezonedb.com/v2.1/convert-time-zone?key={key}&format=json&from={src_timezone}&to={dst_timezone}&time={timestamp}'
# print(api)

print('London sunrise :', datetime.fromtimestamp(timestamp))
print('UTC sunrise :', datetime.fromtimestamp(timestamp))

def jprint(obj):
    # create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

r = requests.get(api)
data = json.loads(r.text)

jprint(data)
print(data['toTimestamp'])

uktd = data['toTimestamp']

print(datetime.fromtimestamp(timestamp))
print(datetime.fromtimestamp(uktd))
