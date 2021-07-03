import subprocess
import multiprocessing as mp

class Node:
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
        # Check status of given links.  
        with subprocess.Popen(['curl', '-r0-0', '--fail','-sS', f'http://{self.node_ip}{link}'],stderr=subprocess.PIPE,stdout=subprocess.PIPE) as proc:
            resp = proc.stderr.read().decode('utf-8')
            if resp != '':
                # TODO: dump status of the node to sqlite                             
                return {link:'FAILED'} 
            else:   
                return {link:'SUCCESS'} 

if __name__ == '__main__':
    a = Node("46.101.96.184")
    with mp.Pool(a.cpu) as pool:
        res = pool.map_async(a.node_status, a.check_links)
        data = res.get()
    all = {k:v for pc in data for k,v in pc.items()}
   
    #print("status:",a.status)
    #a.node_info()
    #print(dic)
    #print(status1)
