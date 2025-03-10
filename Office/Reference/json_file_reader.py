import json
import sys

sys.path.append ('/Users/stevemcgarry/Projects/VS_Python/Tools')
from gyro_tools import *
file = '/Users/stevemcgarry/Projects/Velo-Websockets/Office/output/vce_list.json'

with open(file, 'r', encoding='utf-8') as f:  # Explicit encoding for robustness
    data = json.load(f)
    for i in data:
        jprint(i)