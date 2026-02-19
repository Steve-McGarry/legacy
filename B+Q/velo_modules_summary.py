from variables import *
import sys
import json
import requests

headers = {"Content-Type": "application/json", "Authorization": token}

def get_software_versions():
    get_softwareVersions = f'{vco_url}enterpriseProxy/getEnterpriseProxyOperatorProfiles'
    software_params = {"enterpriseProxyId": 0}
    versions_resp = requests.post(get_softwareVersions, headers=headers, data=json.dumps(software_params))
    software_versions = versions_resp.json()
    
    return software_versions

def get_profiles():
    get_profile_list = f'{vco_url}enterprise/getEnterpriseConfigurationsPolicies'
    profile_params = {
        "enterpriseId": enterprise_id,
    }
    profile_response = requests.post(get_profile_list, headers=headers, data=json.dumps(profile_params))
    prof_response = profile_response.json()
    
    return prof_response

def get_licenses():
    get_license_list = f'{vco_url}license/getEnterpriseEdgeLicenses'
    license_params = {
        "enterpriseId": enterprise_id,
    }
    license_response = requests.post(get_license_list, headers=headers, data=json.dumps(license_params))
    l_response = license_response.json()
    
    return l_response

def create_edge(provision_params):
    new_edge = f'{vco_url}edge/edgeProvision'

    provision_response = requests.post(new_edge, headers=headers, data=json.dumps(provision_params))
    prov_response = provision_response.json()
    
    return prov_response

def update_software_version(fw_version):
    
    update_softwareVersions = f'{vco_url}edge/setEdgeOperatorConfiguration'
    software_versions = get_software_versions()
    
    for version in software_versions:
        if version['name'] == fw_version:
            software_id = version['id']
            print(software_id)

    software_params = {"edgeId": edge_id,
        "enterpriseId": enterprise_id,
        "configurationId": software_id,
    }
    software_resp = requests.post(update_softwareVersions, headers=headers, data=json.dumps(software_params))
    s_resp = software_resp.json()

    return s_resp

def list_edges(enterprise_id):
    get_edges = f'{vco_url}enterprise/getEnterpriseEdgeList'

    getConfig_params = {'enterpriseId': enterprise_id}

    list_reponse = requests.post(get_edges, headers=headers, data=json.dumps(getConfig_params))
    edge_list = list_reponse.json()

    return edge_list

def get_edge(edge_id):
    get_edge = f'{vco_url}/edge/getEdge'

    edge_params = {
        'enterpriseId': enterprise_id,
        'edgeId': edge_id
    }

    call_response = requests.post(get_edge, headers=headers, data=json.dumps(edge_params))

    get_resp = call_response.json()
    return get_resp

def edge_config(edge_id):
    get_edgeconfig = f'{vco_url}edge/getEdgeConfigurationStack'

    config_params = {'edgeId': edge_id,
            'enterpriseId': enterprise_id}

    config_reponse = requests.post(get_edgeconfig, headers= headers, data=json.dumps(config_params))
    c_response = config_reponse.json()
    
    return c_response

def wanLinkSummary(edgeSpecificProfile):
    edgeSpecificProfile = edgeSpecificProfile
    modules = edgeSpecificProfile['modules']
    
    count = 0
    for m in modules:
        if m['name'] == 'WAN':
            wan_links = edgeSpecificProfile['modules'][count]['data']['links']
        else:
            count += 1
    wan_count = (len(wan_links))
    
    network_list = []
    for i in range(wan_count):
            sim_count = 0
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