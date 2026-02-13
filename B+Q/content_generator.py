from variables import *
from velo_modules_summary import *
import jsonpatch

# Std variables
now = datetime.datetime.now()
timestamp = now.strftime('%d%m%y')
output_dir = '/Users/stevemcgarry/Projects/Velo-Websockets/B+Q/output'

# >>> START OF CODE
def edge_list():
        edges_output = f'{output_dir}/vce_list_full-{timestamp}.json'
        edge_list = list_edges(enterprise_id)

        with open(edges_output,'w') as file:
            json.dump(edge_list, file)

        #quick reference list name + id
        vce_dict = {}
        site_count = 0
        for i in edge_list:
            # print(site_count)
            site_count += 1
            vce_dict[f'{i["name"]}'] = i["id"]
        
        print(f'Total number of devices: {site_count}')

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
    edgeSpecificProfile = dict(config_response[0])
    
    with open(output_file,'w') as file:
        json.dump(edgeSpecificProfile, file)
    
    # first instance for config - ignore 2nd
    edgeSpecificProfile = dict(config_response[0])
    edgeSpecificProfileDeviceSettings = (edgeSpecificProfile['modules'])

    module_dict = {}
    for module in edgeSpecificProfileDeviceSettings:
        module_dict.update({module['name']:module['id']})
        if module['name'] == 'deviceSettings':
            device_settings = module['data']
            module_id = module['id']
    
    return device_settings, module_id

# def update_device_config(edge_id)

>>>>>>>>>>> PICKUP FROM HERE !!!!
def create_appliance(appliance_name):
    name = appliance_name
    edgeProvision_params = {
        "enterpriseId": enterprise_id,
        "configurationId": profile_id,
        "edgeLicenseId": license_id,
        "modelNumber": device_type,
        "name": name,
    }

    print(f'Creating edge {name}')

    provision_response = requests.post(create_edge, headers=headers, data=json.dumps(edgeProvision_params))

    p_response = provision_response.json()
    # jprint(p_response)
    
    # >>>>>> capture activation key & hostname ready to email

    with open(exit_log, mode='w') as output_2:
        print(p_response,file=output_2)
    
    if 'error' in p_response:
        # print(f'Error creating edge {d}')
        break

    with open(provision_log, mode='a') as output_1:
        output_1.write(f"{d},{p_response['id']},{p_response['activationKey']}\n")
    
    device_id = p_response['id']
    activation_key = p_response['activationKey']
    new_data = f'    activation_code: {activation_key}\n'

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

    # # checking content
    # print('Verifying updates....')
    # print(f"override: {device_settings['override']}")
    # print(f"Type: {device_settings['routedInterfaces'][lan_index]['addressing']['type']}")
    # print(f"cidrPrefix: {device_settings['routedInterfaces'][lan_index]['addressing']['cidrPrefix']}")
    # print(f"cidrIp: {device_settings['routedInterfaces'][lan_index]['addressing']['cidrIp']}")
    # print(f"netmask: {device_settings['routedInterfaces'][lan_index]['addressing']['netmask']}")
    # print(f"gateway: {device_settings['routedInterfaces'][lan_index]['addressing']['gateway']}")

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


def test():
    pass

def main ():
    # test()
    # ----------------------------
    # clrscr()
    edge_list()
    get_device_info(edge_id)
 
    
if __name__ == "__main__":
    main()