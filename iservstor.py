import ipfsapi
import json
import os
import sqlite3
### Configuration
Cpath = os.path.dirname(os.path.realpath(__file__))
with open(Cpath+'/config.json') as f:
    Jconfig = json.load(f)
IPFS_IP = Jconfig['IPFS_IP']
IPFS_PORT = Jconfig['IPFS_PORT']
class iServStor:
    ### Initialization
    def __init__(self):
        self.api = ipfsapi.connect(IPFS_IP,IPFS_PORT)
    def GetPeers(self):
        Pdict = dict()
        conn = sqlite3.connect(Cpath+'/'+Jconfig['DBpath']+'/Iportal.db')
        c = conn.cursor()
        c.execute("SELECT * FROM Peers WHERE status = 0;") # IP, peerID, status, speed, nextTry
        for x in c:
            Pdict[x[1]] = dict()
            Pdict[x[1]]['IP'] = x[0]
            Pdict[x[1]]['status'] = x[2]
            Pdict[x[1]]['speed'] = x[3]
        return Pdict
