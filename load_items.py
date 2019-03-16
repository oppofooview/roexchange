from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from declare_db import Base, Item 
import argparse
import sys

engine_name = 'sqlite:///exchange.db'

if __name__ == '__main__':
    engine = create_engine(engine_name)
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--item', help='Enter card or mat or bp', default='mat')
    args = vars(parser.parse_args())

    if args['item'] == 'card':
        print('Loading card info into db')
        file_name = 'items/card_info.txt'
        delimiter = '|'
        
        with open(file_name, 'r') as f:
            for line in f:
                line = line.replace('\n', '')
                attrs = line.split(delimiter)
                cardname = attrs[0]
                cardeffect = attrs[1]
                cardunlock = attrs[2]
                carddeposit = attrs[3]
                cardtype = attrs[4]
                cardslot = attrs[5]
                cardrarity = attrs[6]
                cardshortname = cardname.replace(' ', '_').lower()
                
                item = session.query(Item).filter_by(name=cardname).first()
                if not item:
                    newitem = Item(name=cardname, item_type='Card', info_name=cardshortname,
                                unlock_effect=cardunlock, deposit_effect=carddeposit,
                                source=cardtype, slot=cardslot, rarity=cardrarity)
                    session.add(newitem)
        print('Cards loading completed')
    elif args['item'] == 'mat':
        print('Loading mat info into db')
        file_name = 'items/mats.txt'
        with open(file_name, 'r') as f:
            for line in f:
                line = line.replace('\n', '')
                matname = line.replace('_', ' ').capitalize()
                matshortname = line 
                item = session.query(Item).filter_by(name=matname).first()
                if not item:
                    newitem = Item(name=matname, item_type='Mat', info_name=matshortname)
                    session.add(newitem)
        print('Mats loading completed')
    elif args['item'] == 'bp':
        print('Loading bp info into db')
        file_name = 'items/bp.txt'
        with open(file_name, 'r') as f:
            for line in f:
                line = line.replace('\n', '')
                matname = line.replace('_', ' ').capitalize()
                matshortname = line 
                item = session.query(Item).filter_by(name=matname).first()
                if not item:
                    newitem = Item(name=matname, item_type='Blueprint', info_name=matshortname)
                    session.add(newitem)
        print('Blueprint loading completed')
    
    session.commit()
