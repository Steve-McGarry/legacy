import csv
import sys
import os
import json
import datetime
import requests

sys.path.append ('/Users/stevemcgarry/Projects/VS_Python/Tools')
from gyro_tools import *

wl_url = 'https://simpro4.wirelesslogic.com/'
get_sim = 'api/v3/sims'
get_sim_details = 'api/v3/sims/details'
get_sims_api = f'{wl_url}{get_sim}'
get_sim_details = f'{wl_url}{get_sim_details}'
# sim_list = 'sim_list.json'

def wl_lookup(api_name):
    auth_file = '/Users/stevemcgarry/Downloads/MCSHINE/simpro.json'

    with open(auth_file) as file:
            data = json.load(file)

    for provider in data['keys']:
        if provider['target'] == api_name:
            api = provider['api_key']
            client = provider['client_key']
            account = provider['account_number']
    
    return account, client, api

def get_sims(output_file):
    sim_list = output_file
    account_number, client_key, api_key = wl_lookup('simpro')
    headers = {
        "Content-Type": "application/json",
        "x-api-client": client_key,
        "x-api-key": api_key,
        }
    
    getSims_params = {'account_number': account_number, 'custom_field1': ['Office Shoes', 'Office'],
                    'status': 'active'  
                    }

    sims_response = requests.get(get_sims_api, headers=headers, params=getSims_params)
    sims_data = sims_response.json()
    sim_count = sims_data['sim_count']

    with open(sim_list,'w') as file:
        json.dump(sims_data, file)
    
    return sims_data, sim_count

def get_sim_detail(output_file, iccid):
    # sim_list = output_file
    iccid = iccid
    sim_details = output_file
    account_number, client_key, api_key = wl_lookup('simpro')
    headers = {
        "Content-Type": "application/json",
        "x-api-client": client_key,
        "x-api-key": api_key,
        }
    getDetails_params = {'identifiers': iccid}

    detail_response = requests.get(get_sim_details, headers=headers, params=getDetails_params)
    sim_detail_data = detail_response.json()

    with open(sim_details,'w') as file:
        json.dump(sim_detail_data, file)

    return sim_detail_data

