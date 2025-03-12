import csv
import sys
import os
import json
import datetime
import requests

sys.path.append ('/Users/stevemcgarry/Projects/VS_Python/Tools')
from gyro_tools import *

get_sims_api = 'https://simpro4.wirelesslogic.com/api/v3/sims'
get_sim_details_api = 'https://simpro4.wirelesslogic.com/api/v3/sims/details'
get_sim_usage_history_api = 'https://simpro4.wirelesslogic.com/api/v3/sims/usage-history'
get_cell_location_api = 'https://simpro4.wirelesslogic.com/api/v3/sim/cell-location'

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
    sim_list_out = output_file
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

    with open(sim_list_out,'w') as file:
        json.dump(sims_data, file)
    
    return sims_data, sim_count

def get_sim_detail(output_file, iccid):
    # sim_list = output_file
    iccid = iccid
    sim_details_out = output_file
    account_number, client_key, api_key = wl_lookup('simpro')
    headers = {
        "Content-Type": "application/json",
        "x-api-client": client_key,
        "x-api-key": api_key,
        }
    getDetails_params = {'identifiers': iccid}

    detail_response = requests.get(get_sim_details_api, headers=headers, params=getDetails_params)
    sim_detail_data = detail_response.json()

    with open(sim_details_out,'w') as file:
        json.dump(sim_detail_data, file)

    return sim_detail_data

def get_sim_usage(output_file, iccid, month):
    sim_usage_out = output_file
    iccid = iccid
    months = month
    account_number, client_key, api_key = wl_lookup('simpro')
    headers = {
        "Content-Type": "application/json",
        "x-api-client": client_key,
        "x-api-key": api_key,
        }
    
    getSimUsage_params = {'identifiers': iccid, 'month': month}  

    usage_response = requests.get(get_sim_usage_history_api, headers=headers, params=getSimUsage_params)
    usage_data = usage_response.json()

    # with open(sim_usage_out,'w') as file:
    #     json.dump(usage_data, file)

    return usage_data

def get_sim_location(iccid):
    iccid = iccid
    api_query = f'https://simpro4.wirelesslogic.com/api/v3/sims/{iccid}/location'
    account_number, client_key, api_key = wl_lookup('simpro')
    headers = {
        "Content-Type": "application/json",
        "x-api-client": client_key,
        "x-api-key": api_key,
        }
    
    getSimLocation_params = {'identifiers': iccid}

    location_response = requests.get(api_query, headers=headers, params=getSimLocation_params)
    location_data = location_response.json()

    return location_data

def get_cell_location(output_file, iccid, month):
    sim_usage_out = output_file
    iccid = iccid
    months = month
    account_number, client_key, api_key = wl_lookup('simpro')
    headers = {
        "Content-Type": "application/json",
        "x-api-client": client_key,
        "x-api-key": api_key,
        }
    
    getSimUsage_params = {'identifiers': iccid, 'month': month}  

    usage_response = requests.get(get_sim_usage_history_api, headers=headers, params=getSimUsage_params)
    usage_data = usage_response.json()