import ipfsapi
import json
import os
import psycopg2
import signal
from web3 import Web3, HTTPProvider
class Bchain:
    def __init__(self):
        signal.signal(signal.SIGALRM, self.handler)
        self.api = ipfsapi.connect('127.0.0.1','5001')
        self.w3 = Web3(HTTPProvider('http://localhost:3000'))
    def handler(self,signum, frame):
        raise Exception("time out")
    def register(self,fhash):
        try:
            signal.alarm(5)
            Rinfo = self.api.object_get(fhash)
            for x in Rinfo['Links']:
                if x['Name']=='Ehash':
                    Ehash = self.api.object_get(x['Hash'])['Data']
                    Ehash = self.w3.toChecksumAddress(Ehash)
                elif x['Name']=='Enode':
                    Enode = self.api.object_get(x['Hash'])['Data']
                elif x['Name']=='ExternalIP':
                    ExternalIP = self.api.object_get(x['Hash'])['Data']
                elif x['Name']=='peerID':
                    peerID = self.api.object_get(x['Hash'])['Data']
            conn = psycopg2.connect(database="postgres",user="postgres",host="127.0.0.1", port="5432")
            cur = conn.cursor()
            cur.execute("INSERT INTO BruceChain VALUES('"+Ehash+"','"+ExternalIP+"','"+Enode+"','"+peerID+"','"+Rinfo['Data']+"',0);")
            conn.commit()
            return json.dumps({"status": "Success"})
        except Exception as e:
            return json.dumps({"status": "Failed", "log": str(e)})
