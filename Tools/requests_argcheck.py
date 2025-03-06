import requests
import json

def jprint(obj):
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

location = requests.get('http://httpbin.org/get', params={'access_key':'key', 'query':'address'})

print(location.text)