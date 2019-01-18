#!/usr/bin/python3
import requests
import json
import time
import sys
from datetime import datetime

url = "https://api.poporing.life/get_price_history/"
item_list = [
'crystal_mirror',
'soft_feather',
'orc_claw',
'bell',
'rose_quartz',
'antenna',
'cursed_ruby',
'raccoon_leaf',
'bloody_rune',
'light_granule',
'wrapping_lace',
'star_crumb',
'pearl',
'parts',
'heroic_emblem',
'dragon_scale',
'fabric',
'four_leaf_clover',
'emperium',
'steel',
'coal',
'mercury',
'biotite',
'time_twister',
'key_of_clock_tower',
'four_leaf_clover'
]
with open('cards.txt', 'r') as f:
    for card in f:
        card = card.replace('__', '_').replace('\n','')
        item_list.append(card)

for item in item_list:
    print(item)

current_time = datetime.now().strftime('%Y%m%d') 
filename = "results_{0}.txt".format(current_time)
f = open(filename, "w")

try:
    for item in item_list:
        query = url + item
        r = requests.get(query) 
        print("[{0}]: Querying data from the POPORING server...".format(item))
        time.sleep(1)
        if r.status_code:  # Status code of response
            data = r.json()  # Content of response
            print("{0}:".format(data['data']['item_name']))
            f.write("[{0}]\n".format(data['data']['item_name']))
            histories = sorted(data['data']['data_list'], key=lambda i:i['timestamp'], reverse=True)
            for history in histories:
                f.write("{0},{1},{2}\n".format(history['price'], history['volume'], history['timestamp']))
        else:
            print('{} was not found'.format(item))
    print("\n[Done] Data has been saved to {0}".format(filename))
    print("This tool is Just4Fun ~Gat")
    input("Press ENTER to continue...")
except:
    f.close()
finally:
    f.close()
