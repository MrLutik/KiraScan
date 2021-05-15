from subprocess import Popen, PIPE
import re

import requests
import time

class Scan:
    def __init__(self,src='all'):
        self.src = src
        if src == 'peers':
            self.srclist= requests.get('https://testnet-rpc.kira.network/download/peers.txt').text
        elif src == 'snaps':
            self.srclist= requests.get('https://testnet-rpc.kira.network/download/snaps.txt').text
        elif src == 'all':
            self.srclist= requests.get('https://testnet-rpc.kira.network/download/peers.txt').text + \
                          requests.get('https://testnet-rpc.kira.network/download/snaps.txt').text
        
        self.iplist = self._iplist()
        self.iplist_len = len(self.iplist)
        self.ipstr = self._ipstr()

        self.ip_ping={}
            
    def _iplist(self):
        return set([ip[41:-6] for ip in self.srclist.split('\n') if ip != ''])
    def _ipstr(self):
        return ','.join(self._iplist())

    def match(self,ip:str):
        try:
            pocket = Popen(f'ping -q -c 3 {ip}'.split(' '), stdout=PIPE)
            stdout = pocket.communicate()[0]
        except requests.exceptions.RequestException as err:
            print(err)
            pass
        return re.search(rb'(\d+\.\d+)\/(\d+\.\d+)\/(\d+\.\d+)\/(\d+\.\d+)\s+ms', stdout)
    
    def reqip(self, ip:str):
        try:
            req = requests.get(f'http://{ip}:11000/api/kira/status')
        except requests.exceptions.RequestException as err:
            print(err)
            pass
        return req.json(), req.status_code

    def pingall(self): 
        for ip in enumerate(self.iplist):
            matched = self.match(ip[1])
            if not (matched is None):
                (json, status) = self.reqip(ip[1])
                if status == 200: 
                    avg = float(matched.group(2))
                    print(f"PING [{ip[0]} of {self.iplist_len-1}]  {ip[1]} average ping is {avg} ms. Block heigt: {json['sync_info']['latest_block_height']}")
                    ip_dict={f"{ip[1]}":avg}
                    self.ip_ping.update(ip_dict)
            else: 
                pass
                print(f"PING [{ip[0]} of {self.iplist_len-1}]  {ip[1]} FAILED")
        print('\n')
   
    def peerstr(self):
        sorted_peers = dict(sorted(self.ip_ping.items(),key=lambda avg: avg[1]))
        peers_list = list(sorted_peers.keys())
        pub_priv = ''
        counter = 0
        for chunk in range(16,self.iplist_len,16):
            sentry_res = f'Public peers({counter}:{chunk})::'+','.join(peers_list[counter:chunk])+'\n\n'

            priv_res = f'Private peers({counter}:{chunk-8})::'+','.join(peers_list[counter:chunk-8])+'\n'
            pub_priv += sentry_res + priv_res
            priv_res = f'Private peers({chunk-8}:{chunk})::'+','.join(peers_list[chunk-8:chunk])+'\n\n'
            pub_priv += priv_res                     
            counter = chunk      
        return pub_priv
    
    def start(self):
        start = time.perf_counter()
        self.pingall()
        peers = self.peerstr()
        stop = time.perf_counter()
        print(peers)
        timer = stop-start
        print("Done in {:.2f} seconds.".format(timer))
        return 0


if __name__ == '__main__':
    src = Scan('all')
    src.start()

    
 

    


