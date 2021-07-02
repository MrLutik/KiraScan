import subprocess
import multiprocessing as mp
import json


class Node:
    '''Collect all data from node and dump it to json'''
    def __init__(self,ip) -> None:
        self.node_ip = ip
        self.cpu = mp.cpu_count()

    check_links = [
                    ":16657/status", # SEED node
                    ":26657/status", # Sentry port
                    ":36657/status", # Priv_sentry port
                    ":56657/status", # Validator port | Minimal node
                    ":11000/api/kira/status",
                    ":11000/api/status",
                    ":11000/download/peers.txt",
                    ":11000/download/snapshot.zip"
                    ]

    def node_status(self,link) -> dict:
        # Check status of given links. Add them to dict. 
        # TODO: dump it to json

        with subprocess.Popen(['curl', '-r0-0', '--fail','-sS', f'http://{self.node_ip}{link}'],stderr=subprocess.PIPE,stdout=subprocess.PIPE) as proc:
            resp = proc.stderr.read().decode('utf-8')
            if resp != '':
                print(link, 'FAILED')
            else:
                print(link, 'SUCCESS')
 

if __name__ == '__main__':
    a = Node("213.136.81.248")
    with mp.Pool(a.cpu) as pool:
        res = pool.map_async(a.node_status, a.check_links)
        res.get()

    #a.node_info()
    #print(dic)
    #print(status1)
