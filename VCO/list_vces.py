import sys
import os
import datetime
import json
import re
import requests

sys.path.append ('/Users/stevemcgarry/Projects/VS_Python/Tools')
from vco_request import VcoRequestManager
from gyro_tools import *

VCO_HOSTNAME = 'vco84-fra1.velocloud.net'
# VCO_HOSTNAME = 'vco211-fra1.velocloud.net'
ENTERPRISE_ID = 43 #GyroDemo 211
ENTERPRISE_ID = 681 #KF 84
OUTPUT_FILE = './VCE/v1/output_84/vce_list.json'
# OUTPUT_FILE = './VCE/v1/output_211/vce_list.json'

EMAIL = 'steve.mcgarry@kerv.com'
PASSWD = ''
auth_file = '/Users/stevemcgarry/Downloads/MCSHINE/access_testing.json'

class ApiException(Exception):
    pass

# GyroCustom
def jprint(obj):
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

def main():
    client = VcoRequestManager(VCO_HOSTNAME)
    
    EMAIL, PASSWD = auth_template()
    # print(f'Password is: {PASSWD}')
    client.authenticate(EMAIL, PASSWD, is_operator=os.environ.get('VC_OPERATOR', False))
    res = client.call_api("enterprise/getEnterpriseEdgeList", { "enterpriseId": ENTERPRISE_ID })

    with open(OUTPUT_FILE, 'w') as output:
        json.dump(res, output)
    
    with open(OUTPUT_FILE) as file:
        data = json.load(file)
        jprint(data)

if __name__ == "__main__":
    main()
