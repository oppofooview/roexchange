import re
import time
import traceback
import argparse
import requests, json 

nowtime = int(time.time()) 
cardfile = 'items/cards.txt'
matfile = 'items/mats.txt'
bpfile = 'items/bp.txt'

def get_cards():
    url = "https://api.poporing.life/get_item_list"
    r = requests.get(url)
    if r.status_code:
        data = r.json()['data']
        item_list = data['item_list']
        cards = [x for x in item_list if 'Card' in x['item_type']]
        card_names = [x['name'] for x in cards]
        with open(cardfile, 'w') as f:
            for c in card_names:
                f.write('{}\n'.format(c))

        print('Completed getting card info')

def get_mats():
    url = "https://api.poporing.life/get_item_list"
    r = requests.get(url)
    if r.status_code:
        data = r.json()['data']
        item_list = data['item_list']
        mats = [x for x in item_list if x['item_type']=='Material']
        mat_names = [x['name'] for x in mats]
        with open(matfile, 'w') as f:
            for c in mat_names:
                f.write('{}\n'.format(c))

        print('Completed getting mat info')

def get_bp():
    url = "https://api.poporing.life/get_item_list"
    r = requests.get(url)
    if r.status_code:
        data = r.json()['data']
        item_list = data['item_list']
        bp = [x for x in item_list if x['item_type']=='Blueprint']
        bp_names = [x['name'] for x in bp]
        with open(bpfile, 'w') as f:
            for c in bp_names:
                f.write('{}\n'.format(c))

        print('Completed getting bp info')
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--type', help='Enter Material or Card or Blueprint or All', default='Material')
    args = vars(parser.parse_args())

    if args['type'] == 'Material':
        print('Getting material names from poporing')
        get_mats()

    if args['type'] == 'Card':
        print('Getting card names from poporing')
        get_cards()

    if args['type'] == 'Blueprint':
        print('Getting blueprint names from poporing')
        get_bp()

    if args['type'] == 'All':
        print('Getting all names from poporing')
        get_mats()
        get_cards()
        get_bp()


