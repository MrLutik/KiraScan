
import requests
import random
import multiprocessing as mp

from requests.api import get

bulk = set()
path = set()

cpu = mp.cpu_count()

def getip(resp:requests.get):
    p = resp.text.split('\n')
    p.remove('')
    peers = {ip[41:-6] for ip in p}
    return peers

def getpeers(ip):
    resp = requests.get("https://testnet-rpc.kira.network/download/peers.txt")
    m = getip(resp)
    return m, ip


def randomip():
    global path, cpu, bulk
    bundle = list() 
    n = 0
    while True:
        ip = random.sample(list(bulk),k=1)
        if ip[0] not in path:
            bundle.append(ip)
            n += 1
        if n == cpu:
            break
    return bundle

def update():
    pass

    
def getall():
    global bulk,path,cpu
    while True:
        with mp.Pool(cpu) as pool:
            result = pool.map_async(getpeers, randomip())
            for r in result.get():
                print('size:', len(r[0]))
                path.update(r[1])
                print(len(bulk - r[0]))
                bulk.update(bulk - r[0])
            print(f'Hunted {len(path)} ips')
            print(f'Total  {len(bulk)} ips')

        
bulk.update(getpeers("75.119.150.233")[0])
getall()



