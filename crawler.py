import time
import requests
import random
import multiprocessing as mp
from sqlalchemy import create_engine, update, insert
from kiradb import node_status
from sqlalchemy.exc import IntegrityError
from kirascan import Node

from requests.api import get

bulk = set()
path = set()

cpu = mp.cpu_count()

def getip(resp:requests.get):
    p = resp.text.split('\n')
    p.remove('')
    peers = {ip[41:-6] for ip in p}
    return peers

def getpeers(ip, init=False):
    if init:
        resp = requests.get("https://testnet-rpc.kira.network/download/peers.txt")
        m = getip(resp)
        return m, ip
    else:
        try:
            resp = requests.get(f"http://{ip}:11000/download/peers.txt", timeout=1)
            m = getip(resp)
            print(f"{ip}:SUCCESS")
            return m, ip
        except Exception as e:
            print(f"{ip}:FAILED")
            return '', ip

def randomip():
    global path, cpu, bulk
    bundle = list() 
    n = 0
    while True:
        ip = random.sample(list(bulk),k=1)
        if ip[0] not in path:
            bundle.append(ip[0])
            n += 1
        if n == cpu:
            break
    return bundle

def updateglob(data):                   
    for n in range(0,cpu):
        for ips in data[n]:
            if isinstance(ips,set):
                bulk.update(ips)
            else:
                path.add(ips)

    
def getall():
    global bulk,path,cpu
    while True:
        with mp.Pool(cpu) as pool:
            result = pool.map_async(getpeers, randomip())
            data = result.get()
        updateglob(data)
        print('Total:',len(bulk),'Checked:', len(path))
        if bulk == path or len(path) >= len(bulk):
            pool.close()
            break

def statustodb(ip):
    n = Node(ip)
    val_data = n.status()
    engine = create_engine('sqlite:///kira.db')
    ins = node_status.insert().values(
                    node_ip = ip,
                    proposer = val_data["proposer"],
                    seed_16657 = val_data[":16657/status"], # SEED node
                    sentry_26657 = val_data[":26657/status"], # Sentry port
                    priv_sentry_36657 = val_data[":36657/status"], # Priv_sentry port
                    snap_46657 = val_data[":46657/status"], # Validator port | Minimal node
                    validator_56657 = val_data[":56657/status"],
                    api_kira_status = val_data[":11000/api/kira/status"],
                    api_status = val_data[":11000/api/status"],
                    download_peers = val_data[":11000/download/peers.txt"],
                    download_snapshot = val_data[":11000/download/snapshot.zip"],
                    )
    try:                
        result = engine.execute(ins)    
        print('INSERTED',result.inserted_primary_key)

    except IntegrityError:
        upd = update(node_status).where(node_status.c.node_ip ==  ip)
        upd = upd.values(
                    proposer = val_data["proposer"],
                    seed_16657 = val_data[":16657/status"], # SEED node
                    sentry_26657 = val_data[":26657/status"], # Sentry port
                    priv_sentry_36657 = val_data[":36657/status"], # Priv_sentry port
                    snap_46657 = val_data[":46657/status"], # Validator port | Minimal node
                    validator_56657 = val_data[":56657/status"],
                    api_kira_status = val_data[":11000/api/kira/status"],
                    api_status = val_data[":11000/api/status"],
                    download_peers = val_data[":11000/download/peers.txt"],
                    download_snapshot = val_data[":11000/download/snapshot.zip"],
                    )
        result = engine.execute(upd)
        print('UPDATED:', result.last_updated_params())

                

if __name__ == '__main__':
    start1 = time.perf_counter()        
    bulk.update(getpeers("75.119.150.233", init=True)[0])
    getall()
    print(f'Done in {time.perf_counter() - start1} sec')
    start2 = time.perf_counter()
    for ip in bulk:
        print('Ip to update:',ip)
        statustodb(ip)
    print(f"Done {time.perf_counter() - start2} sec. Total time: {time.perf_counter() - start1}")