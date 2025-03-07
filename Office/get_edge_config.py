import sys
import json
from pathlib import Path
import requests
import datetime
import csv

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

wan_links = edgeSpecificProfile['modules'][5]['data']['links']
wan_count = (len(wan_links))

network_list = []
for i in range(wan_count):
        sublist = []
        sublist.append(wan_links[i]['name'])
        sublist.append(wan_links[i]['publicIpAddress'])
        sublist.append(wan_links[i]['type'])
        sublist.append(wan_links[i]['isp'])
        sublist.append(wan_links[i]['interfaces'][0])
        # > last avtive time
        # last = (edgeSpecificProfile['modules'][5]['data']['links'][i]['lastActive'])
        # date_time = datetime.datetime.fromtimestamp(last/1000)
        # formatted_date = date_time.strftime('%Y-%m-%d')
        # sublist.append(formatted_date)
        backup = (wan_links[i]['backupOnly'])
        standby = (wan_links[i]['hotStandby'])
        if backup or standby:
                sublist.append('Yes')
        else:
                sublist.append('No')
        network_list.append(sublist)

# >>> prep csv export
testname = 'hostname'
headers = ['site_name', 'wan0_label', 'wan0_ip', 'wan0_type', 'wan0_isp', 'wan0_interface', 'backup/standby',
        'wan1_label', 'wan1_ip', 'wan1_type', 'wan1_isp', 'wan1_interface', 'backup/standby',
        'wan2_label', 'wan2_ip', 'wan2_type', 'wan2_isp', 'wan2_interface', 'backup/standby']
csvline = testname

links = 1
while links <= wan_count:
        csvline = f'{csvline},{network_list[links - 1][0]}'
        csvline = f'{csvline},{network_list[links - 1][1]}'
        csvline = f'{csvline},{network_list[links - 1][2]}'
        csvline = f'{csvline},{network_list[links - 1][3]}'
        csvline = f'{csvline},{network_list[links - 1][4]}'
        csvline = f'{csvline},{network_list[links - 1][5]}'
        links += 1

row_data = csvline.split(',')

with open(f'{base_output}/device_wan-links.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerow(row_data)