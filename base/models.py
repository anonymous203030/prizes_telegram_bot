from datetime import date

from sqlalchemy import Integer, Column, String, ForeignKey, create_engine, MetaData, Table, Date, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

engine = create_engine('sqlite:///sqlite.db', echo = True)
meta = MetaData()

User = Table('User', meta,
             Column('id', Integer, primary_key = True),
             Column('username', String, nullable = False),
             Column('salary', Integer, default = 0),
             )

Item = Table('Item', meta,
             Column('id', Integer, primary_key = True),
             Column('item', String, nullable = False),
             Column('date', Date, default=date),
             Column('owner', String, ForeignKey('User.username'))
             )

meta.bind = engine
meta.create_all(engine)

conn = engine.connect()
