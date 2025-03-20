import json
import sys
import datetime

sys.path.append ('/Users/stevemcgarry/Projects/VS_Python/Tools')
from gyro_tools import *
from wl_modules import *
from velo_modules import *

now = datetime.datetime.now()
timestamp = now.strftime('%d%m%y')
output_dir = '/Users/stevemcgarry/Projects/Velo-Websockets/SimPro/output'
vco = 'vco211-fra1.velocloud.net'
enterprise = 945
api_key = f'Token {api_template("velo_211")}'

sim_list = f'{output_dir}/sim_list-{timestamp}.json'
iccid_list = f'{output_dir}/sim_list_iccid-{timestamp}.json'
sim_details = f'{output_dir}/sim_detail-{timestamp}.json'
sim_usage = f'{output_dir}/sim_usage-{timestamp}.json'
csv_file = f'{output_dir}/device_wan-links-{timestamp}.csv'

## >>>>> START OF CODE
clrscr()
print('\nREPORT GENERATION STARTED\n')
count,vce_dict = listEdges(vco,enterprise,api_key,output_dir,timestamp)
print('List of edges discovered...')
print(f'Sites found: {count}\n')

##  open csv file add header then loop through devices
csv_headers = ['site_name', 'wan_total', 'wan0_label', 'wan0_ip', 'wan0_type', 'wan0_isp', 'wan0_interface', 'backup/standby',
                'wan1_label', 'wan1_ip', 'wan1_type', 'wan1_isp', 'wan1_interface', 'backup/standby',
                'wan2_label', 'wan2_ip', 'wan2_type', 'wan2_isp', 'wan2_interface', 'backup/standby', 'sim_total']

## VELO SUMMARY info to link with WL summary later
velo_brief = {}
with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(csv_headers)
        for key,value in vce_dict.items():
            edge_name = key
            edge_id = value
            print(f'{edge_name} - {edge_id}')
            edgeSpecificProfile = getEdgeConfig(vco,enterprise,api_key,output_dir,timestamp,edge_name,edge_id)
            wan_count, network_list = wanLinkSummary(edgeSpecificProfile)
            # velo_brief[edge_name] = sim_count
            
            #  generate csv content
            csv_line = edge_name
            csv_line = f'{csv_line},{wan_count}'
            links = 0
            # while links + 1 <= wan_count:
            #     network = network_list[links]
            #     sim_count = 0 # outer counter
            #     # counter = 0
            #     print(f'work list {links + 1}: {network}')
            #     print(network_list[links - 1][3])
                
            #     counter = 0 # inner counter
            #     print(len(network))
            #     # while counter < len(network):
            #     #     if network[3] == 'Wireless Logic':
            #     #     # if network_list[links - 1][3] == 'Wireless Logic':
            #     #         counter += 1
            #     #         print(f'found wireless logic sim')
            #     #     else:
            #     #         print('no SIM')
                
            #     # print(counter)
            #     links += 1
            
            # print(sim_count)
            # ***
            links = 1
            # sim_total = 0
            # for network in network_list:
            #     if network_list[links - 1][3] == 'Wireless Logic':
            #         sim_count += 1
            while links <= wan_count:
                csv_line = f'{csv_line},{network_list[links - 1][0]}'
                csv_line = f'{csv_line},{network_list[links - 1][1]}'
                csv_line = f'{csv_line},{network_list[links - 1][2]}'
                csv_line = f'{csv_line},{network_list[links - 1][3]}'
                csv_line = f'{csv_line},{network_list[links - 1][4]}'
                csv_line = f'{csv_line},{network_list[links - 1][5]}'
                links += 1

            row_data = csv_line.split(',')
            writer.writerow(row_data)
            # ***


for e in velo_brief.items():
    print(e)

## WL SUMMARY to link with velo summary
## > get filtered sims list
# sims_data, iccid_nums, sim_count = get_sims(sim_list, iccid_list)
# print(f'Total number of SIMs listed: {sim_count}\n')

# sim_tuple_list = []
# count = 1
# for n in iccid_nums:
#     print(f'> Processing SIM num: {count}')
#     details = sim_detail_extract(n)
#     sim_tuple_list.append((details[0]['custom_field2'],n))
#     count += 1

# ## Iterate through the list of tuples
# site_sim_dict = {}
# for key, value in sim_tuple_list:
#     print(key)
#     if key in site_sim_dict:
#         site_sim_dict[key].append(value)
#     else:
#         site_sim_dict[key] = [value]

# clean_site_sim_dict = {key: value for key, value in site_sim_dict.items() if key[0].isdigit()}
# ## Print dictionary
# print("clean dictionary with lists for duplicate values:")
