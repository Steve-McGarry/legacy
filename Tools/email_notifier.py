import smtplib
import getpass
import json
import os

# setup variables
name = 'mcshineapi@gmail.com'
sender = name
recipient = 'mcshine05@gmail.com'

# establish password (Gmail App Password)
# passw = getpass.getpass(prompt='Enter App code now:')
# passw = ''

with open('/Users/mcshine/Downloads/MCSHINE/api_keys.json', 'r') as file:
        data = json.load(file)

for provider in data['keys']:
        if provider['target'] == 'gmail':
            passw = provider['key']

# prepare connection
smtp_object = smtplib.SMTP('smtp.gmail.com',587)
smtp_object.ehlo()
smtp_object.starttls()

smtp_object.login(name,passw)

# prepare message
os.system('clear')
subject = input('Enter subject of message: ')
content = input ('Type your message in now: ')
# subject = 'start'
# content = 'things'
message = "Subject: "+subject+'\n'+content

smtp_object.sendmail(sender,recipient,message)

print('\nEmail sent closing connection !')
smtp_object.quit()