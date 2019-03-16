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
import sys

db_name = "exchange.db"
engine_name = 'sqlite:///exchange.db'
matsdir = 'dist/images/Materials/'
cardsdir = 'dist/images/Cards/'
bpdir = 'dist/images/Blueprints/'

def query_to_dict(rset):
    result = defaultdict(list)
    for obj in rset:
        instance = inspect(obj)
        for key, x in instance.attrs.items():
            result[key].append(x.value)
    return result

def cleandata(df):
    clean = df.copy()
    clean['datetime'] = pd.to_datetime(clean['timestamp'], unit='s')
    price_mean = clean['price'].groupby(df['item_name']).mean().astype('int64').rename('avg_price')
    price_std = clean['price'].groupby(df['item_name']).std().rename('std_price')
    clean = clean.join(price_mean, on='item_name')
    clean = clean.join(price_std, on='item_name')
    clean = clean[(abs(clean['price'])/abs(clean['avg_price'])>0.2) & (abs(clean['price'])/abs(clean['avg_price'])<5)]
    return clean

def process_df(df):
    processed = df.copy()
    processed['date'] = processed['datetime'].dt.date
    processed = processed.groupby(['item_name', 'date'])['price', 'volume', 'avg_price'].mean().astype('int64')
    return processed

def plot_stats(data):
    today = pd.to_datetime('now').date()
    period = 15
    cutoff = today - pd.to_timedelta(period, unit='d')
    data = data[data['date'] >= cutoff]
    
    fig, ax1 = plt.subplots(figsize=(8, 6))
    plt.xticks(rotation=45)
    ax2 = ax1.twinx()
    ax1.bar(data['date'].apply(mdates.date2num), data['volume'], color=(190/255,190/255,190/255,0.7), label='Volume')
    ax2.plot(data['date'].apply(mdates.date2num), data['price'], label='Price', marker='o')

    # handle the legend
    lines, labels = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax2.legend(lines + lines2, labels + labels2, loc=0)

    # Fix the date format on x-axis
    myFmt = mdates.DateFormatter('%Y-%m-%d')
    ax1.xaxis.set_major_formatter(myFmt)
    
    # Align the 2 y-axis
    #ax1.set_yticks(np.linspace(ax1.get_ybound()[0], ax1.get_ybound()[1], 6))
    #ax2.set_yticks(np.linspace(ax2.get_ybound()[0], ax2.get_ybound()[1], 6))

    # bells and whistles
    ax1.set_title(data.iloc[0]['item_name'], size=20)
    ax1.set_ylabel('Volume', size=15)
    ax2.set_ylabel('Price', size=15)
    ax2.grid(True)

def plot_multi(data, title):
    today = pd.to_datetime('now').date()
    data = data[data['date'] == today].sort_values(by='price')[:10]
    
    fig, ax1 = plt.subplots(figsize=(10, 6))
    plt.xticks(rotation=45)
    ax1.bar(data['item_name'], data['price'], width=0.5)

    # bells and whistles
    ax1.set_title(title, size=20)
    ax1.set_ylabel('Price', size=15)
    ax1.grid(True)

def plot_n_save(item_type, savedir, session):
    items = session.query(Info).join(Item, Info.item_name==Item.info_name).filter(Item.item_type==item_type).all()
    df = pd.DataFrame(query_to_dict(items))
    df = cleandata(df)
    df = process_df(df).reset_index()
    names = df['item_name'].unique()
    dfs = [df[df['item_name']==x] for x in names]
    print(names)

    for df in dfs:
        plot_stats(df)

    for i in plt.get_fignums():
        fig = plt.figure(i)
        axes = fig.axes
        if len(axes) < 1:
            continue
        print('saving figure {}, {}'.format(i, axes[0].get_title()))
        plt.savefig('{}{}.png'.format(savedir, axes[0].get_title()), bbox_inches='tight')

    plt.close('all')

if __name__ == '__main__':
    engine = create_engine(engine_name)
    Base.metadata.bind = engine

    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    #plot_n_save('Mat', matsdir, session)
    #plot_n_save('Blueprint', bpdir, session)

    # create and save plots for cards
    slots = [x[0] for x in session.query(Item.slot).filter(Item.item_type=='Card').distinct().all()]
    for slot in slots:
        c = (session.query(Info).join(Item, Info.item_name==Item.info_name)
                 .filter(Item.item_type=='Card')
                 .filter(Item.slot==slot).all())
        df_slot = pd.DataFrame(query_to_dict(c))
        df_slot = cleandata(df_slot)
        df_slot = process_df(df_slot).reset_index()
        cardnames = df_slot['item_name'].unique()
        carddfs = [df_slot[df_slot['item_name']==x] for x in cardnames]
    
        for carddf in carddfs:
            plot_stats(carddf)
        
        for i in plt.get_fignums():
            fig = plt.figure(i)
            axes = fig.axes
            if len(axes) < 1:
                continue
            print('saving figure {}, {}'.format(i, axes[0].get_title()))
            plt.savefig('{}{}/{}.png'.format(cardsdir, slot, axes[0].get_title()), bbox_inches='tight')

        plt.close('all')    

    rarity = [x[0] for x in session.query(Item.rarity).filter(Item.item_type=='Card').distinct().all()]
    for r in rarity:
        if r == '':
            continue
        c = (session.query(Info).join(Item, Info.item_name==Item.info_name)
                 .filter(Item.item_type=='Card')
                 .filter(Item.rarity==r).all())
        df = pd.DataFrame(query_to_dict(c))
        df = cleandata(df)
        df = process_df(df).reset_index()
        plot_multi(df, r)

    for i in plt.get_fignums():
        fig = plt.figure(i)
        axes = fig.axes
        if len(axes) < 1:
            continue
        print('saving figure {}, {}'.format(i, axes[0].get_title()))
        plt.savefig('{}{}/{}.png'.format(cardsdir, 'rarity', axes[0].get_title()), bbox_inches='tight')
    
    plt.close('all')    
   
    
