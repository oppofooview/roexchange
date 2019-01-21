#!/usr/bin/python3
import requests
import json
import time
import sys
from datetime import datetime

url = "https://api.poporing.life/get_price_history/"
mats_file = 'mats.txt'
cards_file = 'cards.txt'
item_list = []
with open(mats_file, 'r') as f:
    for mat in f:
        mat = mat.replace(' ', '_').replace('\n', '').lower()
        item_list.append(mat)

with open('cards.txt', 'r') as f:
    for card in f:
        card = card.replace('__', '_').replace('\n','')
        item_list.append(card)

#for item in item_list:
    #print(item)
#sys.exit(0)
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
