from jinja2 import Environment, FileSystemLoader

## in code substitution
# environment = Environment()
# template = environment.from_string("Hello, {{ name }}!")
# string = template.render(name="World")
# print(string)

## from template substitution
# path = '/Users/stevemcgarry/Projects/Velo-Websockets/Jinja/'
# environment = Environment(loader=FileSystemLoader(f"{path}templates/"))
# template = environment.get_template("t1.txt")

# user_name = 'Steve'
# account_balance = 100
# update_date = "21st November"

# content = template.render(
#     user_name=user_name,
#     account_balance=account_balance,
#     update_date=update_date
# )

# print(content)

## looping through inputs and generating output

path = '/Users/stevemcgarry/Projects/Velo-Websockets/Jinja/'
output = f'{path}output/'
environment = Environment(loader=FileSystemLoader(f"{path}templates/"))
template = environment.get_template("t1.txt")

inputs = [
    {'user_name': 'Steve', 'account_balance': 100, 'update_date': "21st November"},
    {'user_name': 'Candy', 'account_balance': 200, 'update_date': "21st December"},
    {'user_name': 'Lilly', 'account_balance': 500, 'update_date': "21st January"}
]

for i in inputs:
    filename = f"{output}{i['user_name']}.txt"
    content = template.render(
        user_name=i['user_name'],
        account_balance=i['account_balance'],
        update_date=i['update_date']
    )
    with open(filename, mode="w", encoding="utf-8") as message:
        message.write(content)
        print(f"... wrote {filename}")