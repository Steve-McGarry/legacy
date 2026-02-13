import sys
import datetime
import requests
import json

sys.path.append ('/Users/stevemcgarry/Projects/VS_Python/Tools')
from gyro_tools import *

# >>>vars
vco_hostname = 'vco211-fra1.velocloud.net'
enterprise_id = 43
edge_id = 27901
token = f'Token {api_template("velo_211")}'
vco_url = f'https://{vco_hostname}/portal/rest/'
headers = {"Content-Type": "application/json", "Authorization": token}

# >>>api_calls
get_edge = f'{vco_url}/edge/getEdge'

# get license info
edge_params = {
    'enterpriseId': enterprise_id,
    'edgeId': edge_id
}

call_response = requests.post(get_edge, headers=headers, data=json.dumps(edge_params))
print(call_response.status_code)
print(call_response.reason)
e_resp = call_response.json()

print(token)
print(len(token))
# jprint(e_resp)
print(len(e_resp))
content_str = str(e_resp)
print(len(content_str))
# print(e_resp['name'])
# print(e_resp['modelNumber'])
# print(e_resp['edgeState'])
print(call_response.text)