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
        os.system("mkdir -p "+Cpath+"/"+Jconfig['DBpath'])
        os.system("mkdir -p "+Cpath+"/"+Jconfig['FilePath'])
    def GetGoodPeers(self):
        Pdict = dict()
        speers = self.GetSwarmPeers()
        conn = sqlite3.connect(Cpath+'/'+Jconfig['DBpath']+'/Iportal.db')
        c = conn.cursor()
        c.execute("SELECT * FROM Peers WHERE status = 0;") # IP, peerID, status, speed, nextTry
        for x in c:
            if x[1] not in speers:
                continue
            Pdict[x[1]] = dict()
            Pdict[x[1]]['IP'] = x[0]
            Pdict[x[1]]['status'] = x[2]
            Pdict[x[1]]['speed'] = x[3]
            Pdict[x[1]]['nextTry'] = x[4]
        return Pdict
    def GetSwarmPeers(self):
        Pset = set()
        swarm = self.api.swarm_peers()['Peers']
        for x in swarm:
            Pset.add(x['Peer'])
        return Pset
    def FileUpload(self,Fname):
        result = self.api.add(Cpath+'/'+Jconfig['FilePath']+'/'+Fname)
        Ftype = "dictionary"
        if 'Name' in result:
            result = [result]
            Ftype = "file"
        for x in result:
            if x['Name']==Fname:
                x['type'] = Ftype
                return x
        return {"status": "Failed"}
