# TODO: parse https://testnet-rpc.kira.network/api/valopers?all=true to sqlite; Schedule every 5-10 mins.
from sqlalchemy import create_engine
import requests as rq


req = rq.get("https://testnet-rpc.kira.network/api/valopers?all=true")
json_obj = req.json()
print(json_obj)