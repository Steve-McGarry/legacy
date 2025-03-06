import requests
import json
import sys

def jprint(obj):
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)


key  = 'f692c06e16ba2d80d896d5de745ced98'
address = '8 station road,chertsey,surrey,kt16 8be'
api_url = 'http://api.positionstack.com/v1/'
query_type = 'forward' # address > co-ordinates
address = 'kt16 8be'

query_string = f'{api_url}{query_type}'

print(query_string)

location = requests.get(f'{query_string}', params={'access_key':key, 'query':address})

print(location.status_code)
print(location.content)
content = location.content

original_stdout = sys.stdout
with open('location_info.txt', 'w') as output:
    sys.stdout = output
    print(location.text)
    sys.stdout = original_stdout