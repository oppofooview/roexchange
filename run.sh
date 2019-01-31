#!/bin/bash
python rom_price.py
python load_transactions.py 
python plot.py
./clean_images.sh
./gen_html.sh
mv results*.txt archives/ 
