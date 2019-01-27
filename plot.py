from sqlalchemy import create_engine
from sqlalchemy.inspection import inspect
from declare_db import Base, Info, Item
from sqlalchemy.orm import sessionmaker
from collections import defaultdict
from datetime import datetime
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

db_name = "exchange.db"
engine_name = 'sqlite:///exchange.db'
imagedir = 'dist/images/'

def query_to_dict(rset):
    result = defaultdict(list)
    for obj in rset:
        instance = inspect(obj)
        for key, x in instance.attrs.items():
            result[key].append(x.value)
    return result

def process_df(df):
    processed = df.copy()
    processed = processed.set_index('id')
    processed['datetime'] = pd.to_datetime(processed['timestamp'], unit='s')
    avg_prices = processed.groupby(['item_name'])['price'].mean().astype('int64').rename('avg_price')
    processed = processed.join(avg_prices, on='item_name')
    processed['date'] = processed['datetime'].dt.date
    processed = processed.groupby(['item_name', 'date'])['price', 'volume', 'avg_price'].mean().astype('int64')
    return processed

def plot_stats(data):
    fig, ax1 = plt.subplots(figsize=(8, 6))
    plt.xticks(rotation=45)
    ax2 = ax1.twinx()
    ax1.bar(data['date'].apply(mdates.date2num), data['volume'], color=(190/255,190/255,190/255,0.7), label='Volume')
    ax2.plot(data['date'].apply(mdates.date2num), data['price'], label='Price')

    # handle the legend
    lines, labels = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax2.legend(lines + lines2, labels + labels2, loc=0)

    # Fix the date format on x-axis
    myFmt = mdates.DateFormatter('%Y-%m-%d')
    ax1.xaxis.set_major_formatter(myFmt)
    
    # Align the 2 y-axis
    ax1.set_yticks(np.linspace(ax1.get_ybound()[0], ax1.get_ybound()[1], 6))
    ax2.set_yticks(np.linspace(ax2.get_ybound()[0], ax2.get_ybound()[1], 6))

    # bells and whistles
    ax1.set_title(data.iloc[0]['item_name'])
    ax1.set_ylabel('Volume')
    ax2.set_ylabel('Price')
    ax1.grid(True)

if __name__ == '__main__':
    engine = create_engine(engine_name)
    Base.metadata.bind = engine

    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    mats = session.query(Info).join(Item, Info.item_name==Item.info_name).filter(Item.item_type=='Mat').all()
    df = pd.DataFrame(query_to_dict(mats))
    df = process_df(df).reset_index()
    matnames = df['item_name'].unique()
    matdfs = [df[df['item_name']==x] for x in matnames]

    for matdf in matdfs:
        plot_stats(matdf)
    
    for i in plt.get_fignums():
        plt.figure(i)
        plt.savefig('{}figure_{}.png'.format(imagedir, i))
    
    #plt.tight_layout()
    #plt.show()
