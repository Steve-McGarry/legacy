'''
Reads in file in to memory then performs global search & replace
DO NOT USE IF:
very large file
data is valueable

take a copy first !!!
'''
import shutil

file_name = './test_files/adhoc.txt'
backup = './test_files/adhoc_orig.txt'

# Take a file backup first
shutil.copy2(file_name, backup)

# Read in the file
with open(file_name, 'r') as file :
  filedata = file.read()

# Replace the target string
filedata = filedata.replace('old', 'new')

# Write the file out again
with open(file_name, 'w') as file:
  file.write(filedata)