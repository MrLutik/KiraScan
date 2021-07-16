#!python 

'''Initial database setup'''
from datetime import datetime
from operator import index
from sqlalchemy import (Table, MetaData, Column, String, Integer, Float, create_engine, engine, insert,select)
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import DateTime

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
            Column('commission', Float()),
            Column('status', String(10), index=True),
            Column('rank', Integer()),
            Column('streak',Integer(), index=True),
            Column('mischance', Integer()),
            Column('mischance_confidence', Integer()),
            Column('start_height', Integer()),
            Column('inactive_until', String(25)),
            Column('last_present_block', Integer()),
            Column('missed_blocks_counter', Integer(), index=True),
            Column('produced_blocks_counter', Integer(), index=True),
            Column('top', Integer(),index=True),
            Column('created_on', DateTime(), default=datetime.now),
            Column('updated_on', DateTime(), default=datetime.now, onupdate=datetime.now),
            )


node_status = Table('status', metadata,
            Column('node_ip', String(10), primary_key=True, unique=True),
            Column('proposer', String(41), ForeignKey('validators.proposer')),
            Column('seed_16657', String(8)),
            Column('sentry_26657', String(8)),
            Column('priv_sentry_36657', String(8)),
            Column('snap_46657', String(8)),
            Column('validator_56657',String(8)),
            Column('api_kira_status', String(8)),
            Column('api_status', String(8)),
            Column('download_peers', String(8)),
            Column('download_snapshot', String(8)),
            Column('created_on', DateTime(), default=datetime.now),
            Column('updated_on', DateTime(), default=datetime.now, onupdate=datetime.now),
)
def createtables():
    engine = create_engine('sqlite:///kira.db')
    metadata.create_all(engine)

if __name__ == '__main__':
    createtables()

# TODO: wrap in func or class
# parsing RPC data to DB
#rpc = collectrpc()
#for val_data in rpc['validators']:
#    ins = validators.insert()
#    try:
#        result=engine.execute(ins, val_data)
#    except Exception as e:
#        print(e)
#        pass




#s = select([validators])
#rp=engine.execute(s)
#results = rp.fetchall()
#print(results)    

