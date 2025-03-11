import sys
import datetime
import csv

sys.path.append ('/Users/stevemcgarry/Projects/VS_Python/Tools')
from gyro_tools import *
from velo_modules import *

# >>> Required 
vco = 'vco211-fra1.velocloud.net'
enterprise = 945
api_key = f'Token {api_template("velo_211")}'
output_dir = '/Users/stevemcgarry/Projects/Velo-Websockets/Office/output'
# output_dir = '/Users/stevemcgarry/Projects/Velo-Websockets/Office/output/vce_configs'
now = datetime.datetime.now()
timestamp = now.strftime('%d%m%y')
vce_dict_list = f'{output_dir}/vce_dict.txt'
csv_file = f'{output_dir}/device_wan-links-{timestamp}.csv'

# >>> start of code
clrscr()
print('\nREPORT GENERATION STARTED\n')
count,vce_dict = listEdges(vco,enterprise,api_key,output_dir,timestamp)
with open(vce_dict_list,'w') as dict_file:
    for key, value in vce_dict.items():
        dict_file.write(f'{key}: {value}\n')

print('List of edges discovered...')
print(f'Sites found: {count}\n')

csv_headers = ['site_name', 'wan_total', 'wan0_label', 'wan0_ip', 'wan0_type', 'wan0_isp', 'wan0_interface', 'backup/standby',
                'wan1_label', 'wan1_ip', 'wan1_type', 'wan1_isp', 'wan1_interface', 'backup/standby',
                'wan2_label', 'wan2_ip', 'wan2_type', 'wan2_isp', 'wan2_interface', 'backup/standby']

#  open csv file add header then loop through devices
with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(csv_headers)
        for key,value in vce_dict.items():
            edge_name = key
            edge_id = value
            print(f'{edge_name} - {edge_id}')
            edgeSpecificProfile = getEdgeConfig(vco,enterprise,api_key,output_dir,timestamp,edge_name,edge_id)
            wan_count, network_list = wanLinkSummary(edgeSpecificProfile)
            
            #  generate csv content
            csv_line = edge_name
            csv_line = f'{csv_line},{wan_count}'
            links = 1
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

print('\nREPORT COMPLETED 8-)')