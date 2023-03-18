import re
import requests
import csv
import json


url = 'https://nodes.wavesnodes.com/addresses/data/3P73HDkPqG15nLXevjCbmXtazHYTZbpPoPw'


pattern = re.compile(r'3PHaNgomBkrvEL2QnuJarQVJa71wjw9qiqG_(?!total)([a-zA-Z0-9]+)_(share_tokens_(locked|blocked))')


response = requests.get(url)
data = response.json()


distribution = {}


for item in data:
    match = pattern.match(item["key"])
    if match:
        useraddr = match.group(1)
        amount = int(item["value"])
        if amount != 0:
            if useraddr in distribution:
                distribution[useraddr] += amount
            else:
                distribution[useraddr] = amount




with open('distribution.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['USERADDR', 'AMOUNT'])
    for useraddr, amount in distribution.items():
        writer.writerow([useraddr, amount])


json_data = {'data': []}
for useraddr, amount in distribution.items():
    json_data['data'].append({useraddr: amount})
with open('distribution.json', 'w') as jsonfile:
    json.dump(json_data, jsonfile)
