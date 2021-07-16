from operator import index
from sqlalchemy import create_engine, update, insert
#from sqlalchemy.dialects.sqlite import insert
from sqlalchemy.exc import IntegrityError
from kiradb import validators
import time
import requests as rq
import json
#from kiradb import validators

def collectrpc() -> json:
    while True:
        try:
            req = rq.get('https://testnet-rpc.kira.network/api/valopers?all=true')
            json_obj = req.json()
            break
        except Exception as e:
            print(e)
            time.sleep(100)
    return json_obj

def rpctodb():
    engine = create_engine('sqlite:///kira.db')
    rpc = collectrpc()
    for val_data in rpc['validators']:
        #print(val_data)
        ins = validators.insert()
        try:
            result = engine.execute(ins, val_data)
        except IntegrityError as e:
            pass
        '''
            upd = update(validators).where(validators.c.proposer ==  f"{val_data['proposer']}")
            upd = upd.values(
                top = val_data['top'], 
                commission = val_data['commission'],
                status = val_data['status'],
                rank = val_data['rank'],
                streak = val_data['streak'],
                mischance = val_data['mischance'],
                mischance_confidence = val_data['mischance_confidence'],
                start_height = val_data['start_height'],
                inactive_until = val_data['inactive_until'],
                last_present_block = val_data['last_present_block'],
                missed_blocks_counter = val_data['missed_blocks_counter'],
                produced_blocks_counter = val_data['produced_blocks_counter'],
                )
            result = engine.execute(upd)
            '''

if __name__=='__main__':
    start = time.perf_counter()
    rpctodb()
    stop = time.perf_counter()
    print(f'Done in {stop -start} sec')
        


