import sys
import json
from pathlib import Path
import requests

sys.path.append ('/Users/stevemcgarry/Projects/VS_Python/Tools')
from gyro_tools import *

# >>> Required 
vco_hostname = 'vco211-fra1.velocloud.net'
enterprise_id = 945
edge_id = 35084
token = f'Token {api_template("velo_211")}'
base_output = '/Users/stevemcgarry/Projects/Velo-Websockets/Office/output'
config_output = f'{base_output}/vce_config-{edge_id}.json'

# API call
vco_url = f'https://{vco_hostname}/portal/rest/'
headers = {"Content-Type": "application/json", "Authorization": token}
get_edgeconfig = f'{vco_url}edge/getEdgeConfigurationStack'

getConfig_params = {'edgeId': edge_id,
        'enterpriseId': enterprise_id}

config_reponse = requests.post(get_edgeconfig, headers= headers, data=json.dumps(getConfig_params))
c_resp = config_reponse.json()

with open(config_output,'w') as file:
    json.dump(c_resp, file)

edgeSpecificProfile = dict(c_resp[0])
print('Config captured')
jprint(edgeSpecificProfile)

# module_dict = {}
# edgeSpecificProfileDeviceSettings = (edgeSpecificProfile['modules'])
# for module in edgeSpecificProfileDeviceSettings:
#     module_dict.update({module['name']:module['id']})
#     if module['name'] == 'WAN':
#         edgeSpecificProfileDeviceSettingsData = module['data']
#         wan_module_id = module['id']

# print(len(edgeSpecificProfileDeviceSettingsData))
# print(edgeSpecificProfileDeviceSettingsData)