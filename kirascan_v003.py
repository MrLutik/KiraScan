import re
from sys import stdout
import requests
from subprocess import Popen, PIPE, STDOUT


class Node:
    '''Collect all data from node and dump it to json'''
    def __init__(self,ip) -> None:
        self.node_ip = ip

    check_links = [
                    ":16657/status", # SEED node
                    ":26657/status", # Sentry port
                    ":36657/status", # Priv_sentry port
                    ":56657/status", # Validator port |Minimal node
                    ":11000/api/kira/status",
                    ":11000/api/status",
                    ":11000/download/peers.txt",
                    ]

    def node_status(self) -> dict:
        # Check status of given links. Add them to dict. 
        # TODO: dump it to json
        node_status ={"ip":f"{self.node_ip}"}
        status={}
        for link in Node.check_links:
            try:
                req = requests.get(f"http://{self.node_ip}{link}")
                print(f"http://{self.node_ip}{link}")
                print(link, req.status_code)
            except Exception:
                req = None
            if req:
                #print(req.__dict__)
                d={f"{link}":f"{req.status_code}"}
                status.update(d)
            else:
                d={f"{link}":"FAILED"}
                status.update(d)
        try:
            req = requests.head(f"http://{self.node_ip}:11000/download/snapshot.zip")
            print(f"http://{self.node_ip}:11000/download/snapshot.zip")
        except Exception:
            status.update({":11000/download/snapshot.zip":"FAILED"})
        status.update({":11000/download/snapshot.zip":f"{req.status_code}"})
        node_status["node_status"] = status
        return node_status
    
    def node_info()->dict:
        pass

if __name__ == '__main__':
    a = Node("213.136.81.248")
    print(a.node_status())
    #print(dic)
    #print(status1)
