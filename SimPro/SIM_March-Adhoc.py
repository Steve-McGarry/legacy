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
sim_usage_file = f'{output_dir}/sim_usage/sim_usage-{timestamp}.json'
csv_file = f'{output_dir}/device_wan-links-{timestamp}.csv'
top_csv = f'{output_dir}/top-3months-{timestamp}.csv'
sim_site_map = f'{output_dir}/sim_site_map-{timestamp}.json'

## >>>>> START OF CODE
clrscr()
print('\nREPORT GENERATION STARTED\n')

##  open csv file add header then loop through devices
csv_headers = ['site_name', 'wan_total', 'wan0_label', 'wan0_ip', 'wan0_type', 'wan0_isp', 'wan0_interface', 'backup/standby',
                'wan1_label', 'wan1_ip', 'wan1_type', 'wan1_isp', 'wan1_interface', 'backup/standby',
                'wan2_label', 'wan2_ip', 'wan2_type', 'wan2_isp', 'wan2_interface', 'backup/standby', 'sim_total']

## VELO SUMMARY info to link with WL summary later (last column in CSV = # of WL SIMs in use)
# > get device list
# count,vce_dict = listEdges(vco,enterprise,api_key,output_dir,timestamp)
# print('List of edges discovered...')
# print(f'Sites found: {count}\n')

# > extract wan information for each device
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
#                 csv_line = f'{csv_line},{network_list[links - 1][0]}'# label
#                 csv_line = f'{csv_line},{network_list[links - 1][1]}'#ip
#                 csv_line = f'{csv_line},{network_list[links - 1][2]}'#type
#                 csv_line = f'{csv_line},{network_list[links - 1][3]}'#isp
#                 if network_list[links - 1][3] == 'Wireless Logic':
#                     wl_links += 1
#                 csv_line = f'{csv_line},{network_list[links - 1][4]}'#interface
#                 csv_line = f'{csv_line},{network_list[links - 1][5]}'#standby
#                 links += 1
            
#             csv_line = f'{csv_line},{wl_links}'#append each row with number of WL links
#             row_data = csv_line.split(',')
#             writer.writerow(row_data)

## WL SUMMARY to link with velo summary
## > get filtered sims list
sims_data, iccid_nums, sim_count = get_sims(sim_list, iccid_list)
print(f'Total number of SIMs listed: {sim_count}\n')

# iccid_nums_short = iccid_nums[:5] # test 
sim_tuple_list = []
sim_usage = {}
count = 1

## > Allocate mapping of SIM to site & collect usage data
# for iccid in iccid_nums_short: #test
for iccid in iccid_nums:
    print(f'> Processing SIM num: {count}   {iccid}')
    details = sim_detail_extract(iccid)
    count += 1
    ## generate SIM mappings; tuple of site,iccid
    sim_tuple_list.append((details[0]['custom_field2'],iccid)) 
    
    ## get usage data for each sim; 1,2,3,4 months dict[iccid:[1,2,3,4]]
    ## *** auto month calulator required ***
    for m in 1,2,3,4:
        try:
            sim_usage_data = get_sim_usage(sim_usage, iccid, m)
            down = int(sim_usage_data['sims'][0]['month_to_date_bytes_down'])
            up = int(sim_usage_data['sims'][0]['month_to_date_bytes_up'])
            result = f'{down}:{up}_{up + down}'
            if iccid in sim_usage:
                sim_usage[iccid].append(result)
            else:
                sim_usage[iccid] = [result]
        except (KeyError, TypeError, IndexError) as e:
            print(f"Error processing SIM usage data for month {iccid}: {e}") #new sim no history
            result = f'0:0_0'
            if iccid in sim_usage:
                sim_usage[iccid].append(result)
            else:
                sim_usage[iccid] = [result]

# print(f'SIM usage\n{sim_usage}') # test
# ## Generate complete site/SIM mappings; iterate through the tuples of site,iccid > dict [site_name:[iccid1, iccid2...]]
site_sim_dict = {}
for key, value in sim_tuple_list:
    # print(key) # test
    if key in site_sim_dict:
        site_sim_dict[key].append(value)
    else:
        site_sim_dict[key] = [value]

print(site_sim_dict) # test
## remove any blank, type None or not starting without a store code
clean_site_sim_dict = {key: value for key, value in site_sim_dict.items() if isinstance(key, str) and key and key[0].isdigit()}
# print(clean_site_sim_dict) # test

with open(sim_site_map, 'w') as json_file:
    json.dump(clean_site_sim_dict, json_file, indent=4)

# ## Print dictionary
# print(f'clean sites\n{clean_site_sim_dict}') # test
site_keys = clean_site_sim_dict.keys()

## *** validate SIMs allocated to a site with number of links in Velo Orchestrator ***

site_total = {}

## create previous month usage data
for site_name in site_keys:
    sub_list = [0,0]
    # print(f'site name{site_name}') # test
    # print(f'site details \n {clean_site_sim_dict[site_name]}') # tests
    for i in clean_site_sim_dict[site_name]:
        temp_list = []
        total = int(sim_usage[str(i)][2].split('_')[1]) # Feb number
        converted = bytes_to_gigabytes(total)
        # print(total) # test
        temp_list.append(converted)

        ## last month compared to preceeding
        delta = int(sim_usage[str(i)][2].split('_')[1]) - int(sim_usage[str(i)][1].split('_')[1]) # feb - jan
        trend = bytes_to_gigabytes(delta)
        # print(delta) # test
        temp_list.append(trend)
        # consolidate values for each index: total & delta
        for i in 0,1:
            sub_list[i] = round(sub_list[i] + temp_list[i],2)
    # update master after site completed
    site_total[site_name] = sub_list

print(site_total)
with open(sim_usage_file, 'w') as json_file:
    json.dump(site_total, json_file, indent=4)

top_ranking = sorted(site_total.items(), key=lambda x: x[1], reverse=True)[:10]

## Print the top 5 highest items
top_consumers = []
print("Top 10 highest items:")
for item, value in top_ranking:
    print(f"{item}: {value}")
    top_consumers.append(item)

## create csv for top consumers for previous 3 months
top_csv_headers = ['site_name', 'month1', 'month2', 'month3', 'month4']
with open(top_csv, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(top_csv_headers)
    for t in top_consumers:
        # sim1 = [0,0,0]
        # sim2 = [0,0,0]
        sim1 = [0,0,0,0]
        sim2 = [0,0,0,0]
        count = 1

        for s in clean_site_sim_dict[t]: # assumed max of 2 SIMs
            if count == 1:
                summary = sim1
            else:
                summary = sim2

            for n in 0,1,2,3:
                summary[n] = int(sim_usage[s][n].split('_')[1])
            count += 1
        
        result = []
        for i in range(4): # assumed previous month & current mtd required else range(3) for only historical
            result.append(sim1[i] + sim2[i])

        top_csv_line = f'{t},{result[0]},{result[1]},{result[2]}'  # month1, month2, month3
        top_csv_line = f'{t},{result[0]},{result[1]},{result[2]},{result[3]}' # month1, month2, month3, month4-mtd

        row_data = top_csv_line.split(',')
        writer.writerow(row_data)
    print(f'\nCSV creation completed for Top Talkers')
