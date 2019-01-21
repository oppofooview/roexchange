import sqlalchemy

import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
 
Base = declarative_base()
  
class Info(Base):
    __tablename__ = 'info'
    id = Column(Integer, primary_key=True)
    item_name = Column(String(250))
    timestamp = Column(Integer)
    price = Column(Integer)
    volume = Column(Integer)
    __table_args__ = (UniqueConstraint('item_name', 'timestamp', name='item_timestamp_uc'),
                     )
                  
class Item(Base):
    __tablename__ = 'item'
    id = Column(Integer, primary_key=True)
    name = Column(String(250))
    item_type = Column(String(100))
    info_name = Column(String(250))
    rarity = Column(String(100))
    unlock_effect = Column(String(500))
    deposit_effect = Column(String(500))
    source = Column(String(100))
    slot = Column(String(100))
    __table_args__ = (UniqueConstraint('name', name='item_name_uc'),)

engine = create_engine('sqlite:///exchange.db')
Base.metadata.create_all(engine)
