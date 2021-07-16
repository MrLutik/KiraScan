import requests as rq
import json
import time

def collectrpc() -> json:
    while True:
        try:
            req = rq.get('https://testnet-rpc.kira.network/api/valopers?all=true')
            json_obj = req.json()
            break
        except Exception as e:
            print(e)
            time.sleep(100)
    return json_obj


