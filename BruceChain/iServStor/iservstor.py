import ipfsapi
import json
import paho.mqtt.client as mqtt
import os
import sqlite3
### Configuration
Cpath = os.path.dirname(os.path.realpath(__file__))
with open(Cpath+'/../../config.json') as f:
    Jconfig = json.load(f)
IPFS_IP = Jconfig['IPFS_IP']
IPFS_PORT = Jconfig['IPFS_PORT']
PIN_ADD = "pin_add"
class iServStor:
    ### Initialization
    def __init__(self):
        self.api = ipfsapi.connect(IPFS_IP,IPFS_PORT)
        os.system("mkdir -p "+Cpath+"/"+Jconfig['DBpath'])
        os.system("mkdir -p "+Cpath+"/"+Jconfig['FilePath'])
        self.conn = sqlite3.connect(Cpath+'/'+Jconfig['DBpath']+'/Iportal.db')
        self.c = self.conn.cursor()
        self.c.execute("CREATE TABLE IF NOT EXISTS Peers(IP text, peerID text, status int, speed int, nextTry int, PRIMARY KEY(IP));")
        self.conn.commit()
    def Publish(self, target, channel, message):
        client = mqtt.Client()
        client.max_inflight_messages_set(200000)
        client.connect(target, Jconfig['MQTT_PORT'])
        client.loop_start()
        msg_info = client.publish(channel, message, qos=1)
        if msg_info.is_published() == False:
            msg_info.wait_for_publish()
        client.disconnect()
    #def CallPeer(self,target):
    #    self.Publish(target,"call_peer",Jconfig['ExternalIP'])
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
    def CheckFileLocation(self,Finfo):
        Pset = set()
        result = self.api.dht_findprovs(Finfo['Hash'])
        for x in result:
            if x["Type"]==4:
                Pset.add(x['Responses'][0]['ID'])
        return Pset
    def FileBackup(self,Finfo,cnt):
        Plist = list(self.CheckFileLocation(Finfo))
        gpeers = self.GetGoodPeers()
        for x in Plist: # Remove bad peer from now-backup
            if x not in gpeers.keys():
                Plist.remove(x)
        if len(Plist) >= cnt: # Enough Backup Already
            Finfo['Backup'] = Plist
            return Finfo
        cnt -= len(Plist)
        count = 0
        for x in gpeers:
            try:
                if x in Plist:
                    continue
                self.Publish(gpeers[x]['IP'],PIN_ADD,Finfo['Hash'])
            except:
                continue
            Plist.append(x)
            count += 1
            if count >= cnt:
                break
        Finfo['Backup'] = Plist
        return Finfo
