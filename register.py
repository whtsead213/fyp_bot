import json
from pprint import pprint

accounts = None

with open('accounts.json') as f:
    accounts = json.load(f)
    for ac in accounts:
        #print(type(ac)) #dict
        print(ac)

print(type(accounts))

with open('accounts2.json', 'w') as f:
    json.dump(accounts, f, indent=4)