import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.inspection import inspect
from declare_db import Base, Info
from sqlalchemy.orm import sessionmaker
from collections import defaultdict
from datetime import datetime

import matplotlib.pyplot as plt

db_name = "exchange.db"
engine_name = 'sqlite:///exchange.db'

def query_to_dict(rset):
    result = defaultdict(list)
    for obj in rset:
        instance = inspect(obj)
        for key, x in instance.attrs.items():
            result[key].append(x.value)
    return result

if __name__ == '__main__':
    engine = create_engine(engine_name)
    Base.metadata.bind = engine

    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    rset = session.query(Info).all()
    df = pd.DataFrame(query_to_dict(rset)).set_index('id')
    df['datetime'] = pd.to_datetime(df['timestamp'], unit='s') 
    cm_info = df[df['item_name'] == 'crystal_mirror'].sort_values(by='datetime')
    plt.figure(figsize=(8,6))
    ax1 = plt.subplot(2,1,1)
    cm_info[['datetime', 'price']].plot(ax=ax1, x='datetime', y='price', title='Crystal Mirror Price')
    ax2 = plt.subplot(2,1,2)
    cm_info[['datetime', 'volume']].plot(ax=ax2, x='datetime', y='volume', title='Crystal Mirror Volume')
    plt.tight_layout()
    plt.show()
