from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from declare_db import Base, Info
from datetime import datetime

engine_name = 'sqlite:///exchange.db'
current_time = datetime.now().strftime('%Y%m%d') 
file_name = 'results_{}.txt'.format(current_time)
print(file_name)

engine = create_engine(engine_name)
print(engine)
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

with open(file_name, 'r') as f:
    print('Loading items into db...')
    for line in f:
        if line[0] == '[':
            item = line[1:-2]
            continue
        details = line.split(',')
        timestamp = int(details[2])
        price = int(details[0])
        volume = int(details[1])

        trans = session.query(Info).filter_by(item_name=item, timestamp=timestamp).first()
        if not trans:
            newinfo = Info(item_name=item, timestamp=timestamp, price=price, volume=volume)
            session.add(newinfo)
    print('Items loading completed')

session.commit()
