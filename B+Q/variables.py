import sys

sys.path.append ('/Users/stevemcgarry/Projects/VS_Python/Tools')
from gyro_tools import *

# # velocloud specific
vco = 'https://vco211-fra1.velocloud.net'
vco_hostname = 'vco211-fra1.velocloud.net'
vco_short = vco.removeprefix('https://').removesuffix('.velocloud.net')
vco_url = f'https://{vco_hostname}/portal/rest/'
token = f'Token {api_template("velo_211")}' # api key retrieve external to repo

# # environment specific
enterprise_id = 43 # tenant
edge_id = 42673
# edge_id = 27901
profile_id = 175 # profile #
license_id = 182 # retrieve from get_licenses
device_type = 'edge6X0'
required_software = 'R5260' # replace as needed
# name = 'steve180226'