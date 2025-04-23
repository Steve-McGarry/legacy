# csv_line = '002_Manchester_Arndale,3,Kerv-TRB,95.129.20.46,WIRELESS,Wireless Logic,GE5,Yes,VCG-ADSL,109.68.14.89,WIRED,Vcg Technology Services,GE6,No,Kerv-USB-4G,95.129.20.29,WIRELESS,Wireless Logic,USB1,No'

# # Split the csv_line string by commas into a list
# items = csv_line.split(',')

# # Print each item with a number starting from 1
# for i, item in enumerate(items):
#     print(f"{i}: {item}")
import csv
import json
import sys

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
sim_usage_file = f'{output_dir}/sim_usage/sim_usage-{timestamp}.json'
csv_file = f'{output_dir}/device_wan-links-230425.csv'
# csv_file = f'{output_dir}/device_wan-links-{timestamp}.csv'
top_csv = f'{output_dir}/top-3months-{timestamp}.csv'
sim_site_map = f'{output_dir}/sim_site_map-230425.json'
# sim_site_map = f'{output_dir}/sim_site_map-{timestamp}.json'
keyerrors = f'{output_dir}/keyerrors.txt'

# count,vce_dict = listEdges(vco,enterprise,api_key,output_dir,timestamp)
# print('List of edges discovered...')
# print(f'Sites found: {count}\n')
# print(vce_dict)

csv_headers = ['site_name', 'wan_total', 'wan0_label', 'wan0_ip', 'wan0_type', 'wan0_isp', 'wan0_interface', 'backup/standby',
                'wan1_label', 'wan1_ip', 'wan1_type', 'wan1_isp', 'wan1_interface', 'backup/standby',
                'wan2_label', 'wan2_ip', 'wan2_type', 'wan2_isp', 'wan2_interface', 'backup/standby', 'sim_total']

## clean site mapping from WL
with open(sim_site_map, 'r') as jsonfile:
    clean_site_sim_dict = json.load(jsonfile) 

# print(clean_site_sim_dict['002_Manchester_Arndale'])
# print(len((clean_site_sim_dict['002_Manchester_Arndale'])))

wl_sim_count = 0

# Open the velo wan summary CSV file
with open(csv_file, mode='r', newline='') as csvfile:
    csv_reader = csv.reader(csvfile)
    next(csv_reader) # skip header
    # Iterate through each row in the CSV file
    for i, row in enumerate(csv_reader):
        if i < 1000:  # Check if the current line number is less than 5
            try:
                # print(row)
                velo_sim_count = row[-1]
                site_name = row[0]
                print('\nVelo stats')
                print(velo_sim_count,site_name)
                print('WL stats')
                wl_sim_count = len(clean_site_sim_dict[site_name])
                print(wl_sim_count)
            except KeyError as e:
                print(f"KeyError encountered: {e}")
                with open(keyerrors, mode='a') as textfile:
                    textfile.write(f"{e}\n")
            except Exception as e:
                print(f"An error occurred: {e}")
        else:
            break
    # rows = 0
    # for row in csv_reader:
    #     while rows < 6:
    #         print(row)
    #     #     print(rows)
    #     #     print(row)
    #     #     # velo_sim_count = row[-1]
    #     #     # site_name = row[0]
    #     #     # print(site_name)
    #     #     # print(type(site_name))
    #     #     # print(clean_site_sim_dict[site_name])
    #     #     # wl_sim_count = len[clean_site_sim_dict[site_name]]
    #     #     # print(f'Site: {site_name} - Velo sims: {velo_sim_count} - WL sims {wl_sim_count}')
    #         rows += 1

#         print(row)
#         print(row[-1])

# with open(csv_file, mode='w', newline='') as file:
#         writer = csv.writer(file)
#         writer.writerow(csv_headers)
#         for key,value in vce_dict.items():
#             edge_name = key
#             edge_id = value
#             print(f'{edge_name} - {edge_id}')
#             edgeSpecificProfile = getEdgeConfig(vco,enterprise,api_key,output_dir,timestamp,edge_name,edge_id)
#             wan_count, network_list = wanLinkSummary(edgeSpecificProfile)
            
#             #  generate csv content
#             csv_line = edge_name
#             csv_line = f'{csv_line},{wan_count}'
#             links = 1
#             wl_links = 0

#             while links <= wan_count:
#                 ## label/ip/type/isp/int/standby
#                 csv_line = f'{csv_line},{network_list[links - 1][0]}'
#                 csv_line = f'{csv_line},{network_list[links - 1][1]}'
#                 csv_line = f'{csv_line},{network_list[links - 1][2]}'
#                 csv_line = f'{csv_line},{network_list[links - 1][3]}'
#                 if network_list[links - 1][3] == 'Wireless Logic':
#                     wl_links += 1
#                 csv_line = f'{csv_line},{network_list[links - 1][4]}'
#                 csv_line = f'{csv_line},{network_list[links - 1][5]}'
#                 links += 1
            
#             csv_line = f'{csv_line},{wl_links}'
#             row_data = csv_line.split(',')
#             writer.writerow(row_data)

## testing
# vce_dict = {'002_Manchester_Arndale': 7299, '008_Kings_Road': 19914, '010_Camden': 7594, '011_Portobello_Rd_London': 7595, '015_MeadowHall': 7596}

# for key,value in vce_dict.items():
#     edge_name = key
#     edge_id = value
#     # print(f'{edge_name} - {edge_id}')
#     edgeSpecificProfile = getEdgeConfig(vco,enterprise,api_key,output_dir,timestamp,edge_name,edge_id)
#     wan_count, network_list = wanLinkSummary(edgeSpecificProfile)
    
#     #  generate csv content
#     csv_line = edge_name
#     csv_line = f'{csv_line},{wan_count}'
#     links = 1
#     wl_links = 0

#     while links <= wan_count:
#                 ## label/ip/type/isp/int/standby
#                 csv_line = f'{csv_line},{network_list[links - 1][0]}'
#                 csv_line = f'{csv_line},{network_list[links - 1][1]}'
#                 csv_line = f'{csv_line},{network_list[links - 1][2]}'
#                 csv_line = f'{csv_line},{network_list[links - 1][3]}'
#                 if network_list[links - 1][3] == 'Wireless Logic':
#                     wl_links += 1
#                 csv_line = f'{csv_line},{network_list[links - 1][4]}'
#                 csv_line = f'{csv_line},{network_list[links - 1][5]}'
#                 links += 1
    
#     csv_line = (f'{csv_line},{wl_links}')
#     print(csv_line)
    # print(f'{edge_name} has {wl_links} connected')