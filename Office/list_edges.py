import sys
import json
from pathlib import Path
import requests

sys.path.append ('/Users/stevemcgarry/Projects/VS_Python/Tools')
from gyro_tools import *

# >>> Required 
vco_hostname = 'vco211-fra1.velocloud.net'
enterprise_id = 945
token = f'Token {api_template("velo_211")}'
base_output = '/Users/stevemcgarry/Projects/Velo-Websockets/Office/output'
edges_output = f'{base_output}/vce_list.json'

# >>> API call
vco_url = f'https://{vco_hostname}/portal/rest/'
headers = {"Content-Type": "application/json", "Authorization": token}
get_edgeconfig = f'{vco_url}enterprise/getEnterpriseEdges'

getConfig_params = {'enterpriseId': enterprise_id}

config_reponse = requests.post(get_edgeconfig, headers= headers, data=json.dumps(getConfig_params))
c_resp = config_reponse.json()

with open(edges_output,'w') as file:
    json.dump(c_resp, file)

vce_dict = {}
site_count = 0
for i in c_resp:
    site_count += 1
    vce_dict[f'{i["name"]}'] = i["id"]

print(site_count)