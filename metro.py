from bs4 import BeautifulSoup
from random import randint
import requests
import time
import json

records = {}
base_url = 'https://www.metrovalencia.es/movimientos_tsc.php?tsc='

with open('metro_ids.json', 'r') as f:
    ids_found = json.load(f)

def load(id):
    url = base_url + str(id)
    r = requests.get(url)
    return r.content

def process(s):
    table = s.find('table').contents
    record = []

    for entry in table[1:]:
        entry = str(entry).split('</td><td>')
        entry[0] = entry[0].replace('<tr><td>', '')
        entry[-1] = entry[-1].replace('</td></tr>', '')
        
        record.append(
            {
                'fecha': entry[0], 
                'zona': entry[1],
                'estacion': entry[2], 
                'billete': entry[3], 
                'validacion': entry[4].split(' ')[-1], 
                'saldo': entry[5]
            }
        )
    
    return record

def main(id):
    s = BeautifulSoup(load(id),'html.parser')

    if len(s.find('table').contents) > 1:
        print('[+] {} exists!'.format(id))
        
        ids_found['ids'].append(id)
        ids_found['records'][id] = process(s)

    else:
        print("[-] {} doesn't exists".format(id))
    
    time.sleep(2.5)

[main(randint(1000000000, 3928000000)) for x in range(100)]

with open('metro_ids.json', 'w') as f:
    json.dump(ids_found, f)

print('Done!')