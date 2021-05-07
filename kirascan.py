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
        self.ip_ping={}
            
    def iplist(self):
        return set([ip[41:-6] for ip in self.srclist.split('\n') if ip != ''])
    def ipstr(self):
        return ','.join(self.iplist())
    def pingall(self): 
        iplist = self.iplist()
        iplist_len = len(iplist)
        for ip in enumerate(iplist):

            pocket = Popen(f'ping -q -c 3 {ip[1]}'.split(' '), stdout=PIPE)
            stdout = pocket.communicate()[0]
            match = re.search(rb'(\d+\.\d+)\/(\d+\.\d+)\/(\d+\.\d+)\/(\d+\.\d+)\s+ms', stdout)
            if not (match is None): 
                avg = float(match.group(2))
                print(f"PING [{ip[0]} of {iplist_len-1}]  {ip[1]} average ping is {avg} ms.")
                ip_dict={f"{ip[1]}":avg}
                self.ip_ping.update(ip_dict)
            else: 
                print(f"PING [{ip[0]} of {iplist_len-1}]  {ip[1]} FAILED")
    def peerstr(self):
        sorted_peers = dict(sorted(self.ip_ping.items(),key=lambda avg: avg[1]))
        peers_list = list(sorted_peers.keys())
        return ','.join(peers_list[:20])

if __name__ == '__main__':
    src = Scan('all')
    src.pingall()
    print("Private peers sorted by avg ping: ", src.peerstr())
    
 

    


