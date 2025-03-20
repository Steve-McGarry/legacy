import json
import sys
import datetime

sys.path.append ('/Users/stevemcgarry/Projects/VS_Python/Tools')
from gyro_tools import *
from wl_modules import *

now = datetime.datetime.now()
timestamp = now.strftime('%d%m%y')
output_dir = '/Users/stevemcgarry/Projects/Velo-Websockets/SimPro/output'

sim_list = f'{output_dir}/sim_list-{timestamp}.json'
iccid_list = f'{output_dir}/sim_list_iccid-{timestamp}.json'
sim_details = f'{output_dir}/sim_detail-{timestamp}.json'
sim_usage = f'{output_dir}/sim_usage-{timestamp}.json'

# iccid = 8931082222051647724 # temp for testing

## > get filtered sims list
# sims_data, iccid_data, sim_count = get_sims(sim_list)
# sims_data, iccid_nums, sim_count = get_sims(sim_list, iccid_list)
# print(f'Total number of SIMs listed: {sim_count}\n')
# print(f'ICCID #: {len(iccid_nums)}')
# print(f'iccids: {iccid_nums}')

## > get specific sim detail
# sim_detail_data = get_sim_detail(sim_details, iccid)
# jprint(sim_detail_data)

## > get sim usage (months previous 1/2/3 only)
# sim_usage_data = get_sim_usage(sim_usage, iccid, 1)
# jprint(sim_usage_data)
iccid_list = [89444611503501245581]
# iccid_list = [89444611503501245581,8931082222051647724]
sim_usage = {}
# for iccid in iccid_list:
#     for m in 1,2,3:
#         sim_usage_data = get_sim_usage(sim_usage, iccid, m)
#         jprint(sim_usage)
#         # down = int(sim_usage_data['sims'][0]['month_to_date_bytes_down'])
#         # up = int(sim_usage_data['sims'][0]['month_to_date_bytes_up'])
#         # result = f'{down}:{up}_{up + down}'
#         # if iccid in sim_usage:
#         #     sim_usage[iccid].append(result)
#         # else:
#         #     sim_usage[iccid] = [result]
for m in 12,1,2,3:
    sim_usage_data = get_sim_usage(sim_usage, 89444611503501245581, m)
    data =sim_usage_data['sims'][0]['month_to_date_bytes_down']
    print(f'For Month {m} data consumed was: {data}' )
    # jprint(sim_usage_data['sims'][0]['month_to_date_bytes_down'])
# print(sim_usage_data['sims'][0]['month_to_date_bytes_down'])

# print(f'd:{down}-u:{up}_{up + down}')
## > get sim location
# sim_location_data = get_sim_location(iccid)
# jprint(sim_location_data)