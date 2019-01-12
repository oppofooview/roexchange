import sqlalchemy

import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
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
                  
engine = create_engine('sqlite:///exchange.db')
Base.metadata.create_all(engine)
