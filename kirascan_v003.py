import re
from sys import stdout
import requests
from subprocess import Popen, PIPE, STDOUT

class LinkChecker:

    links_to_check = [
                    ":16657/status", # SEED node
                    ":26657/status", # Sentry port
                    ":36657/status", # Priv_sentry port
                    ":56657/status", # Validator port |Minimal node
                    ":11000/api/kira/status",
                    ":11000/api/status",
                    ":11000/download/peers.txt",
                    #":11000/download/snapshot.zip",
                    ]

    def check(self, ip:str):
        for link in LinkChecker.links_to_check:
            try:
                req = requests.get(f"http://{ip}{link}")
            except Exception:
                req = None
            if req:
                print(req.status_code, link)
            else:
                print(req, link)

a = LinkChecker()
a.check("144.91.74.43")
#print(status1)