#!/usr/bin/python3
import requests
import json
import time
import sys
from datetime import datetime

url = "https://api.poporing.life/get_price_history/"
files = ['items/mats.txt', 'items/cards.txt', 'items/bp.txt']
item_list = []

for f in files:
    with open(f, 'r') as rf:
        for item in rf:
            item_list.append(item.strip())

for item in item_list:
    print(item)

#sys.exit(0)
current_time = datetime.now().strftime('%Y%m%d') 
filename = "results_{0}.txt".format(current_time)
with open(filename, "w") as f:
    for item in item_list:
        query = url + item
        r = requests.get(query) 
        print("[{0}]: Querying data from the POPORING server...".format(item))
        if r.status_code:  # Status code of response
            data = r.json()  # Content of response
            f.write("[{0}]\n".format(data['data']['item_name']))
            histories = sorted(data['data']['data_list'], key=lambda i:i['timestamp'], reverse=True)
            for history in histories:
                f.write("{0},{1},{2}\n".format(history['price'], history['volume'], history['timestamp']))
        else:
            print('{} was not found'.format(item))
    print("\n[Done] Data has been saved to {0}".format(filename))

