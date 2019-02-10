#!/bin/bash
python rom_price.py
python load_transactions.py 
./clean_images.sh
python plot.py
./gen_html.sh
mv results*.txt archives/ 
npm run deploy
