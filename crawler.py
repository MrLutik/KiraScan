import requests
from kirascan import Node
import time
import multiprocessing as mp
from sqlalchemy import create_engine, update, insert
from kiradb import node_status
from sqlalchemy.exc import IntegrityError

cpu = mp.cpu_count()

path = set()
pool = set()
new = set()

resp = requests.get("https://testnet-rpc.kira.network/download/peers.txt")
p = resp.text.split('\n')
p.remove('')
peers = [ip[41:-6] for ip in p]
pool.update(peers)

def statustodb(ip):
    n = Node(f'{ip}')
    val_data = n.status()
    engine = create_engine('sqlite:///kira.db')
    ins = node_status.insert().values(
                    node_ip = ip,
                    proposer = val_data["proposer"],
                    seed_16657 = val_data[":16657/status"], # SEED node
                    sentry_26657 = val_data[":26657/status"], # Sentry port
                    priv_sentry_36657 = val_data[":36657/status"], # Priv_sentry port
                    snap_46657 = val_data[":56657/status"], # Validator port | Minimal node
                    api_kira_status = val_data[":11000/api/kira/status"],
                    api_status = val_data[":11000/api/status"],
                    download_peers = val_data[":11000/download/peers.txt"],
                    download_snapshot = val_data[":11000/download/snapshot.zip"],
                    )
    #print(ins)
    try:
                
        result = engine.execute(ins)
    
        print('INSERTED:',result.inserted_primary_key)
    except IntegrityError as e:
        pass
    '''
        upd = update(node_status).where(node_status.c.node_ip ==  ip)
        upd = upd.values(
                    proposer = val_data["proposer"],
                    seed_16657 = val_data[":16657/status"], # SEED node
                    sentry_26657 = val_data[":26657/status"], # Sentry port
                    priv_sentry_36657 = val_data[":36657/status"], # Priv_sentry port
                    snap_46657 = val_data[":56657/status"], # Validator port | Minimal node
                    api_kira_status = val_data[":11000/api/kira/status"],
                    api_status = val_data[":11000/api/status"],
                    download_peers = val_data[":11000/download/peers.txt"],
                    download_snapshot = val_data[":11000/download/snapshot.zip"],
                    )
        #print(upd)
        result = engine.execute(upd)
        print('UPDATED:', result.last_updated_params())
    '''
def grab(ip) -> set:
    global path, pool
    if ip:
        

        while True:
            try:
                path.update(ip)
                req = requests.get(f"http://{ip}:11000/download/peers.txt", timeout=5)
                if req.status_code == 200:
                    return {ip[41:-6] for ip in req.text.split('\n')}
            except Exception:
                return False
      

while pool:
    print('Pool length:', len(pool))
    a = {pool.pop() for ip in range(cpu)}
    print('Poped ip', a)
    if a not in path:
        path.update(a)
        #n = Node(f'{a}')
        #print(n.status())
        with mp.Pool(cpu) as pol1:
            res = pol1.map_async(grab, a)
            status = res.get()[0]
        #b = grab(a)
        if status:
            status.remove('')
            for ip in a:
                statustodb(ip)
            new.update(pool - status)
            pool.update(status)
            print('New pool length:', len(pool))
            print('New ips found:', len(pool - status))
            print('New var lngth:', len(new))