from datetime import datetime
from operator import index
import re
from sqlalchemy import (Table, MetaData, Column, String, Integer, Float, create_engine, engine, insert,select)
from sqlalchemy.sql.sqltypes import DateTime
import requests as rq

metadata = MetaData()

#TODO: deal with whitelist somehow
validators = Table('validators', metadata,
            Column('proposer', String(41),primary_key=True,nullable=False,unique=True, index=True),
            Column('address', String(44),nullable=False, unique=True, index=True),
            Column('valkey', String(51),nullable=False, unique=True),
            Column('pubkey', String(51),nullable=False, unique=True),
            Column('moniker', String(50)),
            Column('website', String(50)),
            Column('social', String(50)),
            Column('identity', String(50)),
            Column('comission', Float()),
            Column('status', String(10), index=True),
            Column('rank', Integer()),
            Column('streak',Integer(), index=True),
            Column('mischance', Integer()),
            Column('mischance_confidence', Integer()),
            Column('start_heigh', Integer()),
            Column('inactive_until', String(25)),
            Column('last_present_block', Integer()),
            Column('missed_blocks_counter', Integer(), index=True),
            Column('produced_blocks_counter', Integer(), index=True),
            Column('top', Integer(),index=True),
            Column('created_on', DateTime(), default=datetime.now),
            Column('updated_on', DateTime(), default=datetime.now, onupdate=datetime.now),
            )

engine = create_engine('sqlite:///kira.db')
metadata.create_all(engine)

# TODO: wrap in func or class
# parsing RPC data to DB
req = rq.get("https://testnet-rpc.kira.network/api/valopers?all=true")
json_obj = req.json()
for val_data in json_obj['validators']:
    ins = validators.insert()
    result=engine.execute(ins, val_data)



s = select([validators])
rp=engine.execute(s)
results = rp.fetchall()
print(results)    

