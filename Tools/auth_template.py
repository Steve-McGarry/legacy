import json
import os

auth_file = '/Users/mcshine/Downloads/MCSHINE/access_testing.json'

with open(auth_file) as file:
    data = json.load(file)

os.system('clear')
login = input('\n>>> Please enter username to authenticate with: ')
print(login)
passwd = ''

for user in data['users']:
    if user['userId'] == login:
        passwd = user['passwd']

print(passwd)

# AS A FUNCTION
# EMAIL =''
# PASSWD = ''

# def auth_template():
#     global EMAIL
#     global PASSWD
#     auth_file = '/Users/mcshine/Downloads/MCSHINE/access_testing.json'

#     with open(auth_file) as file:
#         data = json.load(file)

#     os.system('clear')
#     EMAIL = input('\n>>> Please enter username to authenticate with: ')

#     for user in data['users']:
#         if user['userId'] == EMAIL:
#             PASSWD = user['passwd']

# auth_template()
# print(PASSWD)