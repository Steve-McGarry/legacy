import csv
import time
import sys
import os
import json
from pathlib import Path
import logging
import datetime
import requests
import jsonpatch
from netaddr import IPNetwork

sys.path.append ('/Users/stevemcgarry/Projects/VS_Python/Tools')
from gyro_tools import *

# >>> Required 
# KervAPI-Test
# vco_hostname = 'vco211-fra1.velocloud.net'
# enterprise_id = 1231
# Kingfisher
vco_hostname = 'vco84-usvi1.velocloud.net'
enterprise_id = 681
edge_id = 9212
token = f'Token {api_template("velo_84")}'
vco_hostname = 'vco84-usvi1.velocloud.net'
enterprise_id = 681

base_output = '/Users/stevemcgarry/Projects/VS_Python/VCE/v1/output_84/'
config_output = f'{base_output}/vce_config-{edge_id}.json'

# API call
vco_url = f'https://{vco_hostname}/portal/rest/'
headers = {"Content-Type": "application/json", "Authorization": token}
get_edgeconfig = f'{vco_url}edge/getEdgeConfigurationStack'

print('Creating edge VARs')
print(f'Enterprise ID:{enterprise_id}')
print(f'Edge ID:{edge_id}')

getConfig_params = {'edgeId': edge_id,
        'enterpriseId': enterprise_id}

config_reponse = requests.post(get_edgeconfig, headers= headers, data=json.dumps(getConfig_params))
c_resp = config_reponse.json()

with open(config_output,'w') as file:
    json.dump(c_resp, file)

edgeSpecificProfile = dict(c_resp[0])
print('Config captured')

# module_dict = {}
# edgeSpecificProfileDeviceSettings = (edgeSpecificProfile['modules'])
# for module in edgeSpecificProfileDeviceSettings:
#     module_dict.update({module['name']:module['id']})
#     if module['name'] == 'WAN':
#         edgeSpecificProfileDeviceSettingsData = module['data']
#         wan_module_id = module['id']

# print(len(edgeSpecificProfileDeviceSettingsData))
# print(edgeSpecificProfileDeviceSettingsData)