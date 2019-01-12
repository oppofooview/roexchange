#!/usr/bin/python3
import requests
import json
import time
url = "https://api.poporing.life/get_price_history/"
item_list = ['crystal_mirror',
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
	'emperium',]

epoch_time = int(time.time())
filename = "results_{0}.txt".format(epoch_time)
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
			f.write("---[{0}]----\n".format(data['data']['item_name']))
			histories = sorted(data['data']['data_list'], key=lambda i:i['timestamp'], reverse=True)
			for history in histories:
				print("\tprice: {0} volume: {1} time: {2}".format(history['price'], history['volume'], time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(history['timestamp']))))
				f.write("\tprice: {0} volume: {1} time: {2}\n".format(history['price'], history['volume'], time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(history['timestamp']))))
			f.write("\n")
			time.sleep(.4)
	print("\n[Done] Data has been saved to {0}".format(filename))
	print("This tool is Just4Fun ~Gat")
	input("Press ENTER to continue...")
except:
		f.close()
finally:
		f.close()
