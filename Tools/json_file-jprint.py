import json
from gyro_tools import *
from pathlib import Path
import os

input_licenses = Path(r'/Users/stevemcgarry/Projects/VS_Python/VCE/v1/Screwfix/screwfix_licenses.json')
input_profiles = Path(r'/Users/stevemcgarry/Projects/VS_Python/VCE/v1/Screwfix/screwfix_profiles.json')
input_edges = Path(r'/Users/stevemcgarry/Projects/VS_Python/VCE/v1/output_211/vce_list.json')
input_sp_appliances = Path(r'/Users/stevemcgarry/Projects/VS_Python/SP/response_get_appliances.json')

test_file = Path(r'/Users/stevemcgarry/Projects/VS_Python/VCE/v1/output_211/ref_applianceConfig.json')

def test():
    with open(test_file) as file:
        data = json.load(file)
    jprint(data)

# UPDATE 'keys' list for values to return
def edge_summary():
    count_e = 0
    with open(input_edges) as device:
        data1 = json.load(device)

    keys1 = ['id', 'name', 'logicalId']

    print(f'\n>>> Device summary')
    for item1 in data1:
            count_e += 1
            print([item1[key1] for key1 in keys1])

    print(f'\nNumber of items {count_e}')

def licenses_summary():
    count1 = 0
    with open(input_licenses) as licenses:
        data1 = json.load(licenses)

    keys1 = ['alias', 'id']

    print(f'\n>>> License summary')
    for item1 in data1:
            count1 += 1
            print([item1[key1] for key1 in keys1])

    print(f'\nNumber of items {count1}')

def profiles_summary():
    count2 = 0
    with open(input_profiles) as profiles:
        data2 = json.load(profiles)

    keys2 = ['name', 'id']

    print(f'\n>>> Profiles summary\n')
    for item2 in data2:
            count2 += 1
            print([item2[key2] for key2 in keys2])

    print(f'\nNumber of items is {count2}\n')

def sp_appliances():
    count3 = 0
    with open(input_sp_appliances) as appliances:
        devices = json.load(appliances)

    keys3 = ['hostName', 'applianceId', 'nePk']

    print(f'\n>>> Appliance summary\n')
    for device in devices:
            count3 += 1
            print([device[key3] for key3 in keys3])

    print(f'\nNumber of appliances are {count3}\n')

def clrscr():
    # Check if Operating System is Mac and Linux or Windows
    if os.name == 'posix':
        _ = os.system('clear')
    else:
        # Else Operating System is Windows (os.name = nt)
        _ = os.system('cls')

def main():
    clrscr()
    # >>>
    # edge_summary()
    # licenses_summary()
    # profiles_summary()
    test()
    # sp_appliances()

if __name__ == "__main__":
    main()