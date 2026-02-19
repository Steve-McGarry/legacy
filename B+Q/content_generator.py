from variables import *
from velo_modules_summary import *
from datetime import datetime
import jsonpatch

# Std variables
now = datetime.now()
timestamp = now.strftime('%d%m%y')
output_dir = '/Users/stevemcgarry/Projects/Velo-Websockets/B+Q/output'

# >>> START OF CODE
def base_collection():
    # # 1)  populate list firmware versions for reference
    # # example code name: R5260-20251105-GA-6fdd8e5039
    software_versions = get_software_versions()
    software_output = f'{output_dir}/software_versions-{timestamp}.json'

    with open(software_output,'w') as file:
            json.dump(software_versions, file)

    compatable_dict = {}
    for v in software_versions:
        if v['name'].startswith(required_software):
            date_split = v['name'].split('-')
            date = date_split[1]
            compatable_dict[date] = [f'{v["name"]}, {v["id"]}']
    print(compatable_dict)
    newest_list = []
    for c in compatable_dict.keys():
        newest_list.append(c)
    
    best_version = (max(newest_list))
    best_id = compatable_dict[best_version][0].split(",")[1]
    print(f'Best code version available is: {compatable_dict[best_version][0].split(",")[0]}')
    print(f'Best code version ID is: {best_id.lstrip()}')

    # # 2) populate list of Profile names for reference
    profile_list = get_profiles()

    profiles_output = f'{output_dir}/profile_list-{timestamp}.json'

    with open(profiles_output,'w') as file:
            json.dump(profile_list, file)

    # 3) populate list of licences for reference
    licenses_list = get_licenses()
    licenses_output = f'{output_dir}/licenses-{timestamp}.json'

    with open(licenses_output, 'w') as file:
            json.dump(licenses_list, file)

def create_appliance(appliance_name):
    name = appliance_name
    output_file = f'{output_dir}/provision_log-{timestamp}.json'
    provision_params = {
        "enterpriseId": enterprise_id,
        "configurationId": profile_id,
        "edgeLicenseId": license_id,
        "modelNumber": device_type,
        "name": name,
    }

    print(f'Creating edge {name}')

    provision_response = create_edge(provision_params)
    jprint(provision_response)
    # # >>>>>> capture activation key & hostname ready to email engineers
    # # batch summary report include name/id/activation key

    report_string = f"{name},{provision_response['id']},{provision_response['activationKey']}\n"

    with open(output_file, mode='a') as log:
        log.write(report_string)
    
    print(report_string)

def get_device_info(edge_id):
    edge_id = edge_id
    output_file = f'{output_dir}/device_info_{timestamp}.json'
    info_resp = get_edge(edge_id)
    jprint(info_resp)

    with open(output_file, 'w') as file:
        json.dump(info_resp, file)

def get_appliance_config(edge_id):
    edge_id = edge_id
    output_file = f'{output_dir}/device_config_{timestamp}.json'
    config_response = edge_config(edge_id)
    jprint(config_response)
    
    with open(output_file,'w') as file:
        json.dump(config_response, file)
    
    # edgeSpecificProfile_complete = dict(config_response)
    
    
    # **** first instance for config - ignore 2nd ****
    edgeSpecificProfile = dict(config_response[0])
    # edgeSpecificProfileDeviceSettings = (edgeSpecificProfile['modules'])

    # module_dict = {}
    # for module in edgeSpecificProfileDeviceSettings:
    #     module_dict.update({module['name']:module['id']})
    #     if module['name'] == 'deviceSettings':
    #         device_settings = module['data']
    #         module_id = module['id']
    
    # return device_settings, module_id
    # return device_settings, module_id

def update_appliance_config(edge_id):
    edge_id = edge_id
    update_edgeconfig = f'{vco_url}configuration/updateConfigurationModule'

    # ingest config item specific dicts; reduce io time
    device_settings, module_id = get_appliance_config()

    # GE3/LAN interface
    lan_nic = device_settings['routedInterfaces'][1]
    # jprint(lan_nic)
    lan_index = 1
    lan_patch = jsonpatch.JsonPatch([
        {"op": "add", "path": f"/override", "value": True},
        {"op": "add", "path": f"/routedInterfaces/{lan_index}/addressing/type", "value": 'STATIC'},
        {"op": "add", "path": f"/routedInterfaces/{lan_index}/addressing/cidrPrefix", "value": '24'},
        {"op": "add", "path": f"/routedInterfaces/{lan_index}/addressing/cidrIp", "value": '172.20.0.20'},
        {"op": "add", "path": f"/routedInterfaces/{lan_index}/addressing/netmask", "value": '255.255.255.0'},
        {"op": "add", "path": f"/routedInterfaces/{lan_index}/addressing/gateway", "value": '172.20.0.1'},
    ])

    patch_set = jsonpatch.JsonPatch([*lan_patch])
    patch_set.apply(device_settings, in_place=True) # over-write

    # checking content
    print('Verifying updates....')
    print(f"override: {device_settings['override']}")
    print(f"Type: {device_settings['routedInterfaces'][lan_index]['addressing']['type']}")
    print(f"cidrPrefix: {device_settings['routedInterfaces'][lan_index]['addressing']['cidrPrefix']}")
    print(f"cidrIp: {device_settings['routedInterfaces'][lan_index]['addressing']['cidrIp']}")
    print(f"netmask: {device_settings['routedInterfaces'][lan_index]['addressing']['netmask']}")
    print(f"gateway: {device_settings['routedInterfaces'][lan_index]['addressing']['gateway']}")

    update_dict = {'data': {}}
    update_dict['data'] = device_settings

    network_update_params = {
    'enterpriseId': enterprise_id,
    'id': module_id,
    'returnData': 'true',
    '_update': update_dict,
    'name': 'deviceSettings'
    }

    config_reponse = requests.post(update_edgeconfig, headers=headers, data=json.dumps(network_update_params))
    network_resp = config_reponse.json()
    jprint(network_resp)

def upgrade_software():
    
    update_software_version(required_software)

def edge_list():
        edges_output = f'{output_dir}/vce_list_full-{timestamp}.json'
        edge_list = list_edges(enterprise_id)

        with open(edges_output,'w') as file:
            json.dump(edge_list, file)

        #quick reference list name + id
        vce_dict = {}
        site_count = 0
        for i in edge_list:
            site_count += 1
            vce_dict[f'{i["name"]}'] = i["id"]
        
        print(f'Total number of devices: {site_count}')

def test():
    pass

def main ():
    # test()
    # ----------------------------
    # clrscr()
    # base_collection()
    # create_appliance(f'steve{timestamp}')
    upgrade_software()
    # get_device_info(edge_id)
    # get_appliance_config()
    # get_appliance_config(edge_id)
    # edge_list()
 
    
if __name__ == "__main__":
    main()