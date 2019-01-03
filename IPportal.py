import base64
import hashlib
import io
import iota
from iota import TryteString
import ipfsapi
import IOTATransaction
import json
import os
import sqlite3
import time
### Configuration
Cpath = os.path.dirname(os.path.realpath(__file__))
with open(Cpath+'/config.json') as f:
    Jconfig = json.load(f)
IPFS_IP = Jconfig['IPFS_IP']
IPFS_PORT = Jconfig['IPFS_PORT']
class IPportal:
    ### Initialization
    def __init__(self, _ip,_groupkey):
        self.ip = _ip
        self.api = ipfsapi.connect(IPFS_IP,IPFS_PORT)
        self.groupkey = _groupkey
        self.GroupHash = self.api.object_put(io.BytesIO(json.dumps({"Data":_groupkey}).encode()))['Hash']
    ### Encoder and decoder
    def IPENCODE(self):
        X = ""
        tmp = self.ip.split(".")
        for x in tmp:
            for i in range(3):
                try:
                    X += chr(int(x[i])+65)
                except:
                    X += 'X'
        return X
    def IPDECODE(self,eip):
        X = ""
        for i in range(12):
            if i%3==0:
                X += "."
            if eip[i]=="X":
                continue
            X += str(ord(eip[i])-65)
        return X[1:]
    def Kencode(self,key, clear):
        enc = []
        for i in range(len(clear)):
            key_c = key[i % len(key)]
            enc_c = chr((ord(clear[i]) + ord(key_c)) % 256)
            enc.append(enc_c)
        return base64.urlsafe_b64encode("".join(enc).encode()).decode()
    def Kdecode(self,key, enc):
        dec = []
        enc = base64.urlsafe_b64decode(enc).decode()
        for i in range(len(enc)):
            key_c = key[i % len(key)]
            dec_c = chr((256 + ord(enc[i]) - ord(key_c)) % 256)
            dec.append(dec_c)
        return "".join(dec)
    ### Get information
    def GetKey(self):
        m = hashlib.md5()
        m.update(self.IPENCODE().encode('utf-8')+self.groupkey.encode('utf-8'))
        md5key = m.hexdigest()
        return str(TryteString.from_unicode(md5key))
    def GetAddress(self):
        return self.IPENCODE()+self.GetKey()+"KEVIN"
    def GetMessageFromAddress(self,address):
        Rdict = dict()
        #ip = self.IPDECODE(address[0:12])
        key = address[12:76]
        Rdict['peerid'] = self.Kencode(self.groupkey,self.api.id()['ID'])
        return json.dumps(Rdict)
    ### Data to tangle
    def ToTheMoon(self,tag):
        GoodPeer = self.GetGoodPeer(tag)
        for x in GoodPeer:
            if self.api.id()['ID'] in x and Jconfig['ExternalIP'] in x:
                return json.dumps({"status": "Failed", "log": "Already on the moon."})
        b = IOTATransaction.IOTATransaction('DontCare')
        To = self.GetAddress()
        Message = self.GetMessageFromAddress(To)
        pt = b.MakePreparingTransaction(To,Message,tag)
        b.SendTransaction([pt])
        return b.GetTransactionHash()
    def CheckPeer(self,address):
        m = hashlib.md5(address[0:12].encode('utf-8')+self.groupkey.encode('utf-8'))
        md5key = m.hexdigest()
        if TryteString.from_unicode(md5key) == address[12:76]:
            return True
        return False
    def GetConnectionInfo(self,address,message):
        Jmessage = json.loads(message)
        ip = self.IPDECODE(address[0:12])
        peerid = self.Kdecode(self.groupkey,Jmessage['peerid'])
        return "/ip4/"+ip+"/tcp/4001/ipfs/"+peerid
    def GetGoodPeer(self,tag):
        PeerDict = dict()
        GoodPeer = set()
        b = IOTATransaction.IOTATransaction('DontCare')
        T = b.GetTransactionsFromTag(tag)
        for x in T:
            Tinfo = b.GetTransactionMessage(x) # address, message, timestamp
            if self.CheckPeer(Tinfo['address']):
                peer = self.GetConnectionInfo(Tinfo['address'],Tinfo['message'])
                ip = Tinfo['address'][0:12]
                if ip in PeerDict:
                    if int(Tinfo['timestamp'])>int(PeerDict[ip]['timestamp']):
                        PeerDict[ip]['peer'] = peer
                        PeerDict[ip]['timestamp'] = Tinfo['timestamp']
                else:
                    PeerDict[ip] = dict()
                    PeerDict[ip]['peer'] = peer
                    PeerDict[ip]['timestamp'] = Tinfo['timestamp']
        for x in PeerDict:
            GoodPeer.add(PeerDict[x]['peer'])
        return GoodPeer
    def ConnectWithPeers(self,pset):
        Rdict = dict()
        peerID = self.api.id()['ID']
        for x in pset:
            try:
                if peerID in x:
                    continue
                output = self.api.swarm_connect(x)['Strings'][0].replace("\n","")
                tmp = output.split(" ")
                if tmp[2]=="success":
                    Rdict[x] = "success"
            except Exception as e:
                Rdict[x] = str(e)
        return Rdict
    #### Local DB
    def LDBupdate(self):
        conn = sqlite3.connect(Cpath+'/Iportal.db')
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS Peers(IP text, peerID text, status int, speed int, nextTry int, PRIMARY KEY(IP));")
        conn.commit()
        IPdict = dict() # IP -> nextTry
        c.execute("SELECT IP,nextTry FROM Peers;")
        for x in c:
            IPdict[x[0]] = x[1]
        GoodPeer = self.GetGoodPeer(Jconfig['Tag'])
        Ntime = int(time.time())
        Delay = 10
        for x in GoodPeer:
            tmp = x.split("/")
            IP = tmp[2]
            peerID = tmp[len(tmp)-1]
            if peerID == self.api.id()['ID']:
                continue
            if IP not in IPdict.keys():
                self.api.swarm_connect(x)
                c.execute("INSERT INTO Peers VALUES('"+IP+"','"+peerID+"',0,0,0);")
                conn.commit()
            else:
                if IPdict[IP] > Ntime:
                    print("KEVIN")
                    continue
            ping = self.api.ping(tmp[len(tmp)-1],count=1)
            if not ping[1]['Success']:
                c.execute("UPDATE Peers SET status=status+1,speed=-1,nextTry=(status+1)*"+str(Delay)+"+"+str(Ntime)+" WHERE IP = '"+IP+"';")
                conn.commit()
            else:
                c.execute("UPDATE Peers SET status=0,speed=0,nextTry="+str(Ntime)+" WHERE IP = '"+IP+"';")
                conn.commit()
        conn.close()
