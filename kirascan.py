import subprocess
import multiprocessing as mp
import requests

class Node:
    def __init__(self,ip) -> None:
        self.node_ip = ip
        global node_ip # multiprocessing variable 
        node_ip = self.node_ip
        self.cpu = mp.cpu_count()

    check_links = [
                    ":16657/status", # SEED node
                    ":26657/status", # Sentry port
                    ":36657/status",
                    ":46657/status", # Priv_sentry port
                    ":56657/status", # Validator port | Minimal node
                    ":11000/api/kira/status",
                    ":11000/api/status",
                    ":11000/download/peers.txt",
                    ":11000/download/snapshot.zip",
                    ":11000/api/faucet"
                    ]

    def _status_check(link) -> dict:

        # Check status of given links.
        global node_ip
        
        with subprocess.Popen(['curl', '-r0-0', '--fail','-m 3','-sS', f'http://{node_ip}{link}'],stderr=subprocess.PIPE,stdout=subprocess.PIPE) as proc:
            resp = proc.stderr.read().decode('utf-8')
            
        if resp != '':
                # TODO: dump status of the node to sqlite                             
            return {link:'FAILED'} 
        else:   
            return {link:'SUCCESS'}

    def _node_status(self) -> dict:
        
        # multiprocessing launch of the node_status function
             

        with mp.Pool(self.cpu) as pool:
            res = pool.map_async(Node._status_check, self.check_links)
            status = res.get()
        return status

    def _validator(self) -> dict:
        
        try:
            req = requests.get(f"http://{self.node_ip}:56657/status",timeout=1)
            data = req.json()
            return {'proposer':data['result']['validator_info']['address'],'node_ip':f"{self.node_ip}"}
        except Exception:
            return {'proposer':'FAILED','node_ip':f"{self.node_ip}"}
    
    #def _faucet(self) -> dict:
    # /api/cosmos/bank/balances/
    # TODO add faucet data. Figure out how to provide val addr to the request
    #    req = requests.g
    # et((f"http://{self.node_ip}:11000/api/faucet"))
    #    faucet = req.json()
    #    return faucet

    def status(self) -> dict:
        
        val = self._validator()
        stat = self._node_status()
        #rint(stat)
        fin = {}
        fin.update(val)
        for v in stat:
            fin.update(v)
        return fin


if __name__ == '__main__':
    a = Node("167.86.78.246")
    for k,v in a.status().items():
        print(k,v)

