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
sim_details = f'{output_dir}/sim_detail-{timestamp}.json'
sim_usage = f'{output_dir}/sim_usage-{timestamp}.json'

iccid = 8931082222051647724 # temp for testing

## > get filtered sims list
# sims_data, sim_count = get_sims(sim_list)
# print(f'Total number of SIMs listed: {sim_count}\n')

## > get specific sim detail
# sim_detail_data = get_sim_detail(sim_details, iccid)
# jprint(sim_detail_data)

## > get sim usage (months previous 1/2/3 only)
sim_usage_data = get_sim_usage(sim_usage, iccid, 1)
jprint(sim_usage_data)

## > get sim location
# sim_location_data = get_sim_location(iccid)
# jprint(sim_location_data)