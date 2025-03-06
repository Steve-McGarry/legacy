import ipaddress

# import source file 
with open('./test_files/IP_list.txt') as file:
    contents = file.readlines()

print(contents)

ip_list = []
for i in contents:
    con = i.strip() #remove newline char
    print(con)
    ip_list.append(con)

print('\nlist contents')
print(ip_list)

print('\nstandard list sort')
print(sorted(ip_list))

print('\nusing ipaddress module in comprehension')
print(sorted([ipaddress.ip_address(addr)] for addr in ip_list))

print('\nip module with just addresses !')
print(sorted(ip_list, key = ipaddress.ip_address))