import sys
import json
from pathlib import Path
import requests
import datetime

sys.path.append ('/Users/stevemcgarry/Projects/VS_Python/Tools')
from gyro_tools import *

def listEdges(vco,enterprise,api_key,output_list,timestamp):
    vco_hostname = vco
    enterprise_id = enterprise
    token = api_key
    base_output = output_list
    suffix = timestamp

    edges_output = f'{base_output}/vce_list_full-{suffix}.json'

    # >>> API call
    vco_url = f'https://{vco_hostname}/portal/rest/'
    headers = {"Content-Type": "application/json", "Authorization": token}
    get_edgeconfig = f'{vco_url}enterprise/getEnterpriseEdges'

    getConfig_params = {'enterpriseId': enterprise_id}

    config_reponse = requests.post(get_edgeconfig, headers= headers, data=json.dumps(getConfig_params))
    c_resp = config_reponse.json()

    with open(edges_output,'w') as file:
        json.dump(c_resp, file)

    #quick reference list name + id
    vce_dict = {}
    site_count = 0
    for i in c_resp:
        site_count += 1
        vce_dict[f'{i["name"]}'] = i["id"]

    return site_count, vce_dict

def getEdgeConfig(vco,enterprise,api_key,output_dir,timestamp,edge_name,edge_id):
    vco_hostname = vco
    enterprise_id = enterprise
    token = api_key
    base_output = output_dir
    suffix = timestamp
    edge_name = edge_name
    edge_id = edge_id

    config_output = f'{base_output}/vce_configs/{edge_name}-{suffix}.json'

    # API call
    vco_url = f'https://{vco_hostname}/portal/rest/'
    headers = {"Content-Type": "application/json", "Authorization": token}
    get_edgeconfig = f'{vco_url}edge/getEdgeConfigurationStack'

    getConfig_params = {'edgeId': edge_id,
            'enterpriseId': enterprise_id}

    config_reponse = requests.post(get_edgeconfig, headers= headers, data=json.dumps(getConfig_params))
    c_resp = config_reponse.json()
    edgeSpecificProfile = dict(c_resp[0])

    with open(config_output,'w') as file:
        json.dump(edgeSpecificProfile, file)
    
    return edgeSpecificProfile

def wanLinkSummary(edgeSpecificProfile):
    edgeSpecificProfile = edgeSpecificProfile
    modules = edgeSpecificProfile['modules']
    
    count = 0
    for m in modules:
        # print(m['name'])
        # print(count)
        if m['name'] == 'WAN':
            # wan_links = f"{edgeSpecificProfile}['modules'][{count}]['data']['links']"
            wan_links = edgeSpecificProfile['modules'][count]['data']['links']
        else:
            count += 1
    # wan_links = edgeSpecificProfile['modules'][5]['data']['links']
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
    
    return wan_count, network_list

def getEdgeApps(vco,enterprise,api_key,edge_id,output_dir,timestamp,start,stop):
    vco_hostname = vco
    enterprise_id = enterprise
    token = api_key
    base_output = output_dir
    suffix = timestamp
    epoch_start = start
    epoch_end = stop

    apps_output = f'{base_output}/app_list-{suffix}.json'

    # >>> API call
    vco_url = f'https://{vco_hostname}/portal/rest/'
    headers = {"Content-Type": "application/json", "Authorization": token}
    get_apps = f'{vco_url}/metrics/getEdgeAppMetrics'

    getApps_params = {
                    'enterpriseId': enterprise_id,
                    'id': edge_id,
                    'interval': {
                        "start": epoch_start,
                        "end": epoch_end
                    },
                    # 'limit': 5,
                    'resolveApplicationNames': True
                    }

    app_reponse = requests.post(get_apps, headers= headers, data=json.dumps(getApps_params))
    a_resp = app_reponse.json()

    with open(apps_output,'w') as file:
        json.dump(a_resp, file)

    return a_resp

def getQOE(vco,enterprise,api_key,edge_id,output_dir,timestamp,start,stop):
    vco_hostname = vco
    enterprise_id = enterprise
    token = api_key
    base_output = output_dir
    suffix = timestamp
    epoch_start = start
    epoch_end = stop

    qoe_output = f'{base_output}/qoe_day-{suffix}.json'

    # >>> API call
    vco_url = f'https://{vco_hostname}/portal/rest/'
    headers = {"Content-Type": "application/json", "Authorization": token}
    get_qoe = f'{vco_url}/linkQualityEvent/getLinkQualityEvents'
    

    getQOE_params = {
                    'enterpriseId': enterprise_id,
                    'edgeId': edge_id,
                    'interval': {
                        "end": epoch_end,
                        "start": epoch_start
                    }
                    }

    qoe_reponse = requests.post(get_qoe, headers=headers, data=json.dumps(getQOE_params))
    q_resp = qoe_reponse.json()

    with open(qoe_output,'w') as file:
        json.dump(q_resp, file)

    return q_resp
