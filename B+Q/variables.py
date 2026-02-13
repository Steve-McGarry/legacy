import sys

sys.path.append ('/Users/stevemcgarry/Projects/VS_Python/Tools')
from gyro_tools import *

# # Velocloud specific
vco = 'https://vco211-fra1.velocloud.net'
vco_hostname = 'vco211-fra1.velocloud.net'
vco_short = vco.removeprefix('https://').removesuffix('.velocloud.net')
vco_url = f'https://{vco_hostname}/portal/rest/'
token = f'Token {api_template("velo_211")}' # api key retrieve external to repo

# environment specific
enterprise_id = 43 # tenant
edge_id = 27901
profile_id = 12345 # profile #
license_id = 54321 # retrieve from get_licenses
device_type = '6x0'
required_software = 123